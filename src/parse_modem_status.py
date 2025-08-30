#!/usr/bin/env python3
"""
Parse cable modem status from HTTP endpoints and output InfluxDB line protocol format.

This script fetches the HTML from a cable modem's status pages and extracts
key metrics for monitoring in InfluxDB, including basic modem information,
connection status, and channel performance metrics.
"""

import re
import sys
import time
import requests
from bs4 import BeautifulSoup


def parse_uptime(uptime_str):
    """
    Parse uptime string like '28 days 18h:10m:50s.00' into seconds.

    Args:
        uptime_str (str): Uptime string from modem

    Returns:
        int: Total uptime in seconds
    """
    total_seconds = 0

    # Extract days
    days_match = re.search(r'(\d+)\s+days?', uptime_str)
    if days_match:
        total_seconds += int(days_match.group(1)) * 86400

    # Extract hours
    hours_match = re.search(r'(\d+)h', uptime_str)
    if hours_match:
        total_seconds += int(hours_match.group(1)) * 3600

    # Extract minutes
    minutes_match = re.search(r'(\d+)m', uptime_str)
    if minutes_match:
        total_seconds += int(minutes_match.group(1)) * 60

    # Extract seconds
    seconds_match = re.search(r'(\d+)s', uptime_str)
    if seconds_match:
        total_seconds += int(seconds_match.group(1))

    return total_seconds


def extract_modem_info(html_content):
    """
    Extract modem information from HTML content.

    Args:
        html_content (str): HTML content from modem status page

    Returns:
        dict: Dictionary containing extracted modem metrics
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tables with class "simpleTable"
    tables = soup.find_all('table', class_='simpleTable')

    data = {}

    for table in tables:
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)

                # Clean up the key (remove "strong" tags, etc.)
                key = re.sub(r'<[^>]+>', '', key)

                # Store the data
                if key and value:
                    data[key] = value

    return data


def extract_channel_info(html_content):
    """
    Extract channel information from connection status HTML content.

    Args:
        html_content (str): HTML content from connection status page

    Returns:
        tuple: (aggregated_data, downstream_channels, upstream_channels)
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tables with class "simpleTable"
    tables = soup.find_all('table', class_='simpleTable')

    downstream_channels = []
    upstream_channels = []

    for table in tables:
        # Check if this is a downstream bonded channels table
        header = table.find('th')
        if header and 'Downstream Bonded Channels' in header.get_text():
            rows = table.find_all('tr')[2:]  # Skip header rows
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 8:
                    channel_data = {
                        'channel_id': cells[0].get_text(strip=True),
                        'lock_status': cells[1].get_text(strip=True),
                        'modulation': cells[2].get_text(strip=True),
                        'frequency': cells[3].get_text(strip=True),
                        'power': cells[4].get_text(strip=True),
                        'snr': cells[5].get_text(strip=True),
                        'corrected': cells[6].get_text(strip=True),
                        'uncorrectables': cells[7].get_text(strip=True)
                    }
                    downstream_channels.append(channel_data)

        # Check if this is an upstream bonded channels table
        elif header and 'Upstream Bonded Channels' in header.get_text():
            rows = table.find_all('tr')[2:]  # Skip header rows
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 7:
                    channel_data = {
                        'channel': cells[0].get_text(strip=True),
                        'channel_id': cells[1].get_text(strip=True),
                        'lock_status': cells[2].get_text(strip=True),
                        'channel_type': cells[3].get_text(strip=True),
                        'frequency': cells[4].get_text(strip=True),
                        'width': cells[5].get_text(strip=True),
                        'power': cells[6].get_text(strip=True)
                    }
                    upstream_channels.append(channel_data)

    # Aggregate channel statistics
    aggregated_data = {}

    if downstream_channels:
        locked_count = sum(1 for ch in downstream_channels if ch['lock_status'] == 'Locked')
        aggregated_data['downstream_channels_total'] = len(downstream_channels)
        aggregated_data['downstream_channels_locked'] = locked_count

        # Calculate average power and SNR for locked channels
        locked_channels = [ch for ch in downstream_channels if ch['lock_status'] == 'Locked']
        if locked_channels:
            try:
                powers = [float(ch['power'].replace(' dBmV', '')) for ch in locked_channels if 'dBmV' in ch['power']]
                snrs = [float(ch['snr'].replace(' dB', '')) for ch in locked_channels if 'dB' in ch['snr']]

                if powers:
                    aggregated_data['downstream_avg_power'] = sum(powers) / len(powers)
                if snrs:
                    aggregated_data['downstream_avg_snr'] = sum(snrs) / len(snrs)

                # Sum up error counts
                corrected_total = sum(int(ch['corrected']) for ch in locked_channels if ch['corrected'].isdigit())
                uncorrectable_total = sum(int(ch['uncorrectables']) for ch in locked_channels if ch['uncorrectables'].isdigit())

                aggregated_data['downstream_corrected_total'] = corrected_total
                aggregated_data['downstream_uncorrectable_total'] = uncorrectable_total
            except (ValueError, TypeError):
                pass  # Skip if parsing fails

    if upstream_channels:
        locked_count = sum(1 for ch in upstream_channels if ch['lock_status'] == 'Locked')
        aggregated_data['upstream_channels_total'] = len(upstream_channels)
        aggregated_data['upstream_channels_locked'] = locked_count

        # Calculate average power for locked channels
        locked_channels = [ch for ch in upstream_channels if ch['lock_status'] == 'Locked']
        if locked_channels:
            try:
                powers = [float(ch['power'].replace(' dBmV', '')) for ch in locked_channels if 'dBmV' in ch['power']]
                if powers:
                    aggregated_data['upstream_avg_power'] = sum(powers) / len(powers)
            except (ValueError, TypeError):
                pass  # Skip if parsing fails

    return aggregated_data, downstream_channels, upstream_channels


def format_influxdb_line(measurement, tags, fields, timestamp=None):
    """
    Format data as InfluxDB line protocol.

    Args:
        measurement (str): InfluxDB measurement name
        tags (dict): Tag key-value pairs
        fields (dict): Field key-value pairs
        timestamp (int, optional): Unix timestamp in nanoseconds

    Returns:
        str: InfluxDB line protocol formatted string
    """
    if timestamp is None:
        timestamp = int(time.time() * 1_000_000_000)  # Convert to nanoseconds

    # Format tags
    tag_str = ""
    if tags:
        tag_pairs = []
        for key, value in tags.items():
            # Escape special characters in tag keys and values
            key = str(key).replace(' ', '_').replace(',', '\\,').replace('=', '\\=')
            value = str(value).replace(' ', '_').replace(',', '\\,').replace('=', '\\=')
            tag_pairs.append(f"{key}={value}")
        tag_str = "," + ",".join(tag_pairs)

    # Format fields
    field_pairs = []
    for key, value in fields.items():
        # Escape special characters in field keys
        key = str(key).replace(' ', '_').replace(',', '\\,').replace('=', '\\=')

        # Determine field type and format accordingly
        if isinstance(value, str):
            # String fields need quotes and escaping
            value = '"' + value.replace('"', '\\"') + '"'
        elif isinstance(value, bool):
            # Boolean fields
            value = str(value).lower()
        elif isinstance(value, (int, float)):
            # Numeric fields
            value = str(value)
        else:
            # Default to string
            value = '"' + str(value).replace('"', '\\"') + '"'

        field_pairs.append(f"{key}={value}")

    field_str = ",".join(field_pairs)

    return f"{measurement}{tag_str} {field_str} {timestamp}"


def format_channel_lines(base_tags, downstream_channels, upstream_channels, timestamp=None):
    """
    Format individual channel data as InfluxDB line protocol.

    Args:
        base_tags (dict): Base tag key-value pairs from modem info
        downstream_channels (list): List of downstream channel data
        upstream_channels (list): List of upstream channel data
        timestamp (int, optional): Unix timestamp in nanoseconds

    Returns:
        list: List of InfluxDB line protocol strings for each channel
    """
    if timestamp is None:
        timestamp = int(time.time() * 1_000_000_000)  # Convert to nanoseconds

    lines = []

    # Format downstream channels
    for channel in downstream_channels:
        tags = base_tags.copy()
        tags['channel_id'] = channel['channel_id']
        tags['direction'] = 'downstream'

        fields = {
            'lock_status': channel['lock_status'],
            'modulation': channel['modulation'],
            'frequency': channel['frequency'],
            'power': channel['power'],
            'snr': channel['snr'],
            'corrected': channel['corrected'],
            'uncorrectables': channel['uncorrectables']
        }

        # Convert numeric values
        try:
            if 'Hz' in channel['frequency']:
                fields['frequency_hz'] = int(channel['frequency'].replace(' Hz', ''))
            if 'dBmV' in channel['power']:
                fields['power_dbmv'] = float(channel['power'].replace(' dBmV', ''))
            if 'dB' in channel['snr']:
                fields['snr_db'] = float(channel['snr'].replace(' dB', ''))
            if channel['corrected'].isdigit():
                fields['corrected_errors'] = int(channel['corrected'])
            if channel['uncorrectables'].isdigit():
                fields['uncorrectable_errors'] = int(channel['uncorrectables'])
        except (ValueError, TypeError):
            pass  # Keep original string values if conversion fails

        line = format_influxdb_line('cable_modem_channel', tags, fields, timestamp)
        lines.append(line)

    # Format upstream channels
    for channel in upstream_channels:
        tags = base_tags.copy()
        tags['channel_id'] = channel['channel_id']
        tags['direction'] = 'upstream'

        fields = {
            'channel': channel['channel'],
            'lock_status': channel['lock_status'],
            'channel_type': channel['channel_type'],
            'frequency': channel['frequency'],
            'width': channel['width'],
            'power': channel['power']
        }

        # Convert numeric values
        try:
            if 'Hz' in channel['frequency']:
                fields['frequency_hz'] = int(channel['frequency'].replace(' Hz', ''))
            if 'Hz' in channel['width']:
                fields['width_hz'] = int(channel['width'].replace(' Hz', '').replace(' kHz', '000'))
            if 'dBmV' in channel['power']:
                fields['power_dbmv'] = float(channel['power'].replace(' dBmV', ''))
        except (ValueError, TypeError):
            pass  # Keep original string values if conversion fails

        line = format_influxdb_line('cable_modem_channel', tags, fields, timestamp)
        lines.append(line)

    return lines


def main():
    """Main function to fetch and parse modem status."""
    urls = [
        "http://192.168.100.1/cmswinfo.html",
        "http://192.168.100.1/cmconnectionstatus.html"
    ]

    all_modem_data = {}
    downstream_channels = []
    upstream_channels = []

    for url in urls:
        try:
            # Fetch the HTML content
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Extract modem information
            modem_data = extract_modem_info(response.text)
            channel_data = {}

            if modem_data:
                all_modem_data.update(modem_data)

            # Extract channel information if this is the connection status page
            if 'cmconnectionstatus.html' in url:
                channel_data, downstream_channels, upstream_channels = extract_channel_info(response.text)
                all_modem_data.update(channel_data)

            # Only report no data if both modem_data and channel_data are empty for this URL
            if not modem_data and not channel_data:
                print(f"No data extracted from {url}", file=sys.stderr)

        except requests.RequestException as exception:
            print(f"Error fetching modem status from {url}: {exception}", file=sys.stderr)
            continue

    if not all_modem_data:
        return 1

    # Extract specific metrics for InfluxDB
    tags = {}
    fields = {}

    # Set up tags (static identifiers)
    if 'Cable Modem MAC Address' in all_modem_data:
        tags['mac_address'] = all_modem_data['Cable Modem MAC Address']

    if 'Serial Number' in all_modem_data:
        tags['serial_number'] = all_modem_data['Serial Number']

    if 'Hardware Version' in all_modem_data:
        tags['hardware_version'] = all_modem_data['Hardware Version']

    # Set up fields (metrics that change over time)
    if 'Software Version' in all_modem_data:
        fields['software_version'] = all_modem_data['Software Version']

    if 'Standard Specification Compliant' in all_modem_data:
        fields['docsis_version'] = all_modem_data['Standard Specification Compliant']

    if 'Up Time' in all_modem_data:
        uptime_seconds = parse_uptime(all_modem_data['Up Time'])
        fields['uptime_seconds'] = uptime_seconds
        fields['uptime_raw'] = all_modem_data['Up Time']

    # Add connection status information
    if 'Connectivity State' in all_modem_data:
        fields['connectivity_state'] = all_modem_data['Connectivity State']

    if 'Boot State' in all_modem_data:
        fields['boot_state'] = all_modem_data['Boot State']

    if 'Configuration File' in all_modem_data:
        fields['configuration_file'] = all_modem_data['Configuration File']

    if 'Security' in all_modem_data:
        fields['security'] = all_modem_data['Security']

    if 'DOCSIS Network Access Enabled' in all_modem_data:
        fields['docsis_network_access'] = all_modem_data['DOCSIS Network Access Enabled']

    # Add channel metrics
    for key in ['downstream_channels_total', 'downstream_channels_locked', 'upstream_channels_total', 'upstream_channels_locked',
                'downstream_avg_power', 'downstream_avg_snr', 'upstream_avg_power',
                'downstream_corrected_total', 'downstream_uncorrectable_total']:
        if key in all_modem_data:
            fields[key] = all_modem_data[key]

    # Add a status field to indicate the modem is online
    fields['status'] = 1

    # Generate InfluxDB line protocol for aggregated data
    line = format_influxdb_line("cable_modem_status", tags, fields)
    print(line)

    # Generate InfluxDB line protocol for individual channels
    if downstream_channels or upstream_channels:
        channel_lines = format_channel_lines(tags, downstream_channels, upstream_channels)
        for channel_line in channel_lines:
            print(channel_line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
