#!/usr/bin/env python3
"""
Parse cable modem status from HTTP endpoint and output InfluxDB line protocol format.

This script fetches the HTML from a cable modem's status page and extracts
key metrics for monitoring in InfluxDB.
"""

import requests
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys


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


def main():
    """Main function to fetch and parse modem status."""
    url = "http://192.168.100.1/cmswinfo.html"
    
    try:
        # Fetch the HTML content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Extract modem information
        modem_data = extract_modem_info(response.text)
        
        if not modem_data:
            print("No data extracted from modem status page", file=sys.stderr)
            return 1
        
        # Extract specific metrics for InfluxDB
        tags = {}
        fields = {}
        
        # Set up tags (static identifiers)
        if 'Cable Modem MAC Address' in modem_data:
            tags['mac_address'] = modem_data['Cable Modem MAC Address']
        
        if 'Serial Number' in modem_data:
            tags['serial_number'] = modem_data['Serial Number']
        
        if 'Hardware Version' in modem_data:
            tags['hardware_version'] = modem_data['Hardware Version']
        
        # Set up fields (metrics that change over time)
        if 'Software Version' in modem_data:
            fields['software_version'] = modem_data['Software Version']
        
        if 'Standard Specification Compliant' in modem_data:
            fields['docsis_version'] = modem_data['Standard Specification Compliant']
        
        if 'Up Time' in modem_data:
            uptime_seconds = parse_uptime(modem_data['Up Time'])
            fields['uptime_seconds'] = uptime_seconds
            fields['uptime_raw'] = modem_data['Up Time']
        
        # Add a status field to indicate the modem is online
        fields['status'] = 1
        
        # Generate InfluxDB line protocol
        line = format_influxdb_line("cable_modem_status", tags, fields)
        print(line)
        
        return 0
        
    except requests.RequestException as e:
        print(f"Error fetching modem status: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error processing modem data: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
