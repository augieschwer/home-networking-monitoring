# home-networking-monitoring
Documentation and configuration for monitoring my home network and devices on the network; including PurpleAir sensors, and Google Wifi devices, and an Arris SB8200 cable modem.

## Setup

### Minikube

https://minikube.sigs.k8s.io/docs/start/

### InfluxDB

https://docs.influxdata.com/platform/install-and-deploy/deploying/kubernetes/

```
helm repo add influxdata https://helm.influxdata.com/
helm repo update
helm install myinfluxdb influxdata/influxdb2
```

### Telegraf

https://github.com/influxdata/helm-charts/tree/master/charts/telegraf

```
helm upgrade --install mytelegraf -f configs/helm/telegraf.yaml influxdata/telegraf
```

### Graphana

https://github.com/grafana/helm-charts/blob/main/charts/grafana/README.md

```
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install mygraphana -f configs/helm/graphana.yaml grafana/grafana
```

#### Set up Ingress on Minikube

```
minikube addons enable ingress
minikube service mygraphana-grafana --url
```

#### Dashboards

[Preconfigured dashboards](configs/graphana)

##### PurpleAir

![pa_dash-1](https://github.com/user-attachments/assets/32b86b3c-ab78-4a0f-a007-7f82f1e5da0f)
![pa_dash-2](https://github.com/user-attachments/assets/a3ca79a2-743e-44ea-8bc6-052a61b0eb72)
![pa_dash-3](https://github.com/user-attachments/assets/f6f60941-584f-4c6f-b3a2-9dae007a726a)

##### Google Wifi

![Screenshot from 2025-07-06 14-48-07](https://github.com/user-attachments/assets/385af34e-9c31-4ad7-ab29-b3a44f469209)
![Screenshot from 2025-07-06 14-48-36](https://github.com/user-attachments/assets/e5f34aac-64b8-42a1-afe8-8f6126c7a3b3)

##### SB8200

<img width="839" height="958" alt="Screenshot from 2025-07-10 13-47-12" src="https://github.com/user-attachments/assets/8cd29ed0-ce6e-4d84-8f7f-69f92eb09cf7" />
<img width="836" height="920" alt="Screenshot from 2025-07-10 13-48-32" src="https://github.com/user-attachments/assets/ba539867-bfec-44b2-82b7-bae741aec3dc" />
<img width="840" height="919" alt="Screenshot from 2025-07-10 13-49-35" src="https://github.com/user-attachments/assets/6f30d5a8-c233-40f5-9527-fd5abdd2e0bf" />


## Cable Modem Status Parser

The `parse_modem_status.py` script parses HTML status pages from cable modems and outputs comprehensive metrics in InfluxDB line protocol format.

### Features

- Fetches modem status from multiple HTTP endpoints
- Parses HTML tables to extract key metrics and connection status
- Extracts detailed channel performance data (downstream/upstream)
- Converts uptime strings to seconds
- Calculates aggregated channel statistics (power, SNR, error counts)
- Outputs data in InfluxDB line protocol format
- Handles network errors gracefully with fallback support

### Usage

```bash
python3 parse_modem_status.py
```

### Output Format

The script outputs InfluxDB line protocol with the following structure:

#### Aggregated Modem Status

**Measurement**: `cable_modem_status`

**Tags** (static identifiers):
- `mac_address`: Cable modem MAC address
- `serial_number`: Device serial number  
- `hardware_version`: Hardware version

**Fields** (metrics):
- `software_version`: Current software/firmware version
- `docsis_version`: DOCSIS specification compliance
- `uptime_seconds`: Uptime in seconds (numeric)
- `uptime_raw`: Raw uptime string from modem
- `connectivity_state`: Connection state (e.g., "OK")
- `boot_state`: Boot state (e.g., "OK")
- `configuration_file`: Configuration file status
- `security`: Security status (e.g., "Enabled")
- `docsis_network_access`: DOCSIS network access status
- `downstream_channels_total`: Total number of downstream channels
- `downstream_channels_locked`: Number of locked downstream channels
- `upstream_channels_total`: Total number of upstream channels
- `upstream_channels_locked`: Number of locked upstream channels
- `downstream_avg_power`: Average downstream power in dBmV
- `downstream_avg_snr`: Average downstream SNR in dB
- `upstream_avg_power`: Average upstream power in dBmV
- `downstream_corrected_total`: Total corrected errors across all downstream channels
- `downstream_uncorrectable_total`: Total uncorrectable errors across all downstream channels
- `status`: Always 1 (indicates modem is online)

#### Individual Channel Data

**Measurement**: `cable_modem_channel`

**Tags**:
- `mac_address`: Cable modem MAC address
- `serial_number`: Device serial number
- `hardware_version`: Hardware version
- `channel_id`: Unique identifier for the channel
- `direction`: Channel direction (`downstream` or `upstream`)

**Fields** (downstream channels):
- `lock_status`: Lock status of the channel
- `modulation`: Modulation type (e.g., "QAM256", "Other")
- `frequency`: Frequency (raw string)
- `power`: Power level in string format
- `snr`: Signal-to-noise ratio in string format
- `corrected`: Corrected errors (raw string)
- `uncorrectables`: Uncorrectable errors (raw string)
- `frequency_hz`: Frequency in Hz (numeric)
- `power_dbmv`: Power in dBmV (numeric)
- `snr_db`: SNR in dB (numeric)
- `corrected_errors`: Corrected errors (numeric)
- `uncorrectable_errors`: Uncorrectable errors (numeric)

**Fields** (upstream channels):
- `channel`: Channel number
- `lock_status`: Lock status of the channel
- `channel_type`: Channel type (e.g., "SC-QAM", "OFDM Upstream")
- `frequency`: Frequency (raw string)
- `width`: Channel width (raw string)
- `power`: Power level in string format
- `frequency_hz`: Frequency in Hz (numeric)
- `width_hz`: Channel width in Hz (numeric)
- `power_dbmv`: Power in dBmV (numeric)

### Example Output

#### Aggregated Modem Status
```
cable_modem_status,mac_address=C8:63:FC:A2:1F:C5,serial_number=A4M5J1685600275,hardware_version=6 software_version="D31CM-PEREGRINE-1.1.1.0-GA-11-NOSH",docsis_version="Docsis 3.1",uptime_seconds=2562712,uptime_raw="29 days 15h:51m:52s.00",downstream_channels_total=32,downstream_channels_locked=32,upstream_channels_total=4,upstream_channels_locked=4,downstream_avg_power=7.45,downstream_avg_snr=40.39,upstream_avg_power=43.75,downstream_corrected_total=291944657,downstream_uncorrectable_total=2492218,status=1 1751996138995393024
```

#### Individual Channel Data
```
cable_modem_channel,mac_address=C8:63:FC:A2:1F:C5,serial_number=A4M5J1685600275,hardware_version=6,channel_id=33,direction=downstream lock_status="Locked",modulation="Other",frequency="741000000 Hz",power="8.9 dBmV",snr="40.0 dB",corrected="312906486",uncorrectables="56",frequency_hz=741000000,power_dbmv=8.9,snr_db=40.0,corrected_errors=312906486,uncorrectable_errors=56 1751999730941605888

cable_modem_channel,mac_address=C8:63:FC:A2:1F:C5,serial_number=A4M5J1685600275,hardware_version=6,channel_id=1,direction=upstream channel="1",lock_status="Locked",channel_type="SC-QAM",frequency="12400000 Hz",width="3200000 Hz",power="41.0 dBmV",frequency_hz=12400000,width_hz=3200000,power_dbmv=41.0 1751999550196814080
```

**Note**: The script outputs one aggregated status line followed by individual lines for each channel (typically 32 downstream + 4 upstream = 36 channel lines).

### Data Sources

The script fetches data from two endpoints on the cable modem:

1. **`http://192.168.100.1/cmswinfo.html`** - Basic modem information including:
   - Hardware and software versions
   - MAC address and serial number
   - DOCSIS version compliance
   - Uptime information

2. **`http://192.168.100.1/cmconnectionstatus.html`** - Connection status and channel data including:
   - Startup procedure status (connectivity, boot state, configuration)
   - Downstream bonded channels (power levels, SNR, error counts)
   - Upstream bonded channels (power levels, frequency, channel types)
   - Security and network access status

### Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Integration with InfluxDB

To send data directly to InfluxDB:

```bash
# Send to InfluxDB via HTTP API
python3 parse_modem_status.py | curl -i -XPOST 'http://localhost:8086/write?db=networking' --data-binary @-

# Or use with Telegraf exec input plugin
# Add to telegraf.conf:
[[inputs.exec]]
  commands = ["python3 /path/to/parse_modem_status.py"]
  timeout = "30s"
  data_format = "influx"
```

### Monitoring and Alerting

The comprehensive metrics enable effective monitoring of cable modem health:

#### Aggregated Monitoring
**Key Metrics to Monitor:**
- **Channel Lock Status**: `downstream_channels_locked` and `upstream_channels_locked` should equal their respective totals
- **Signal Quality**: `downstream_avg_power` (typically 7-10 dBmV) and `downstream_avg_snr` (>30 dB preferred)
- **Error Rates**: Monitor `downstream_corrected_total` and `downstream_uncorrectable_total` for increasing error counts
- **Connectivity**: `connectivity_state` and `boot_state` should be "OK" for healthy operation

**Alerting Examples:**
- Alert if `downstream_channels_locked` < `downstream_channels_total` (indicates channel bonding issues)
- Alert if `downstream_avg_snr` < 25 dB (poor signal quality)
- Alert if `downstream_avg_power` < 5 dBmV or > 15 dBmV (signal level issues)
- Alert on rapid increases in uncorrectable error rates

#### Individual Channel Monitoring
**Per-Channel Metrics:**
- **Lock Status**: Monitor individual channels for `lock_status != "Locked"`
- **Power Levels**: Track `power_dbmv` for each channel (downstream: 6-10 dBmV, upstream: 35-50 dBmV)
- **Signal Quality**: Monitor `snr_db` for each downstream channel (>30 dB preferred)
- **Error Rates**: Track `corrected_errors` and `uncorrectable_errors` growth per channel
- **Frequency Stability**: Monitor `frequency_hz` for unexpected changes

**Per-Channel Alerting:**
- Alert if any channel has `lock_status != "Locked"`
- Alert if downstream `power_dbmv` < 5 or > 15 for any channel
- Alert if downstream `snr_db` < 25 for any channel
- Alert if upstream `power_dbmv` < 30 or > 55 for any channel
- Alert on rapid increases in per-channel error rates

## Testing

Grab the [augieschwer/telegraf-modem-monitor](https://hub.docker.com/r/augieschwer/telegraf-modem-monitor) image; which is based off of the official Telegraf image and includes the code to retrieve the stats from the sb8200.

```
docker pull augieschwer/telegraf-modem-monitor
docker run -v ./configs/telegraf:/etc/telegraf/telegraf.d/ augieschwer/telegraf-modem-monitor --test --config-directory /etc/telegraf/telegraf.d/
```

## Nerdy details

[PurpleAir Sensor JSON Documentation](https://community.purpleair.com/t/sensor-json-documentation/6917)

[Getting more info from your Google Nest Wifi Pro devices](https://www.googlenestcommunity.com/t5/Nest-Wifi/Getting-more-info-from-your-Google-Nest-Wifi-Pro-devices/m-p/343797)
