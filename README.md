# home-networking-monitoring
Documentation and configuration for monitoring my home network and devices on the network; including PurpleAir sensors, and Google Wifi devices.

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


## Cable Modem Status Parser

The `parse_modem_status.py` script parses HTML status pages from cable modems and outputs key metrics in InfluxDB line protocol format.

### Features

- Fetches modem status from HTTP endpoint
- Parses HTML tables to extract key metrics
- Converts uptime strings to seconds
- Outputs data in InfluxDB line protocol format
- Handles network errors gracefully

### Usage

```bash
python3 parse_modem_status.py
```

### Output Format

The script outputs InfluxDB line protocol with the following structure:

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
- `status`: Always 1 (indicates modem is online)

### Example Output

```
cable_modem_status,mac_address=C8:63:FC:A2:1F:C5,serial_number=A4M5J1685600275,hardware_version=6 software_version="D31CM-PEREGRINE-1.1.1.0-GA-11-NOSH",docsis_version="Docsis 3.1",uptime_seconds=2484908,uptime_raw="28 days 18h:15m:08s.00",status=1 1751918337127612928
```

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

##### Nerdy details

[PurpleAir Sensor JSON Documentation](https://community.purpleair.com/t/sensor-json-documentation/6917)

[Getting more info from your Google Nest Wifi Pro devices](https://www.googlenestcommunity.com/t5/Nest-Wifi/Getting-more-info-from-your-Google-Nest-Wifi-Pro-devices/m-p/343797)
