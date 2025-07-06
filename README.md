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

![pa_dash-1](https://github.com/user-attachments/assets/32b86b3c-ab78-4a0f-a007-7f82f1e5da0f)
![pa_dash-2](https://github.com/user-attachments/assets/a3ca79a2-743e-44ea-8bc6-052a61b0eb72)
![pa_dash-3](https://github.com/user-attachments/assets/f6f60941-584f-4c6f-b3a2-9dae007a726a)

##### Nerdy details

[PurpleAir Sensor JSON Documentation](https://community.purpleair.com/t/sensor-json-documentation/6917)

