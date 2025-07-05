# home-networking-monitoring
Documentation and configuration for monitoring my home network and devices on the network.

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
