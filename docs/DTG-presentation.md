# My Overly Complicated Home Networking and Monitoring Project

*Featuring MoCA magic, AI coding assistance, and hard-learned lessons about ISP truck rolls*

---

## 1. The "Problem" (2 minutes)

### The Setup That Worked Fine
<img width="191" height="442" alt="network-1 drawio" src="https://github.com/user-attachments/assets/e9529259-8863-4982-a3d6-8a0f196b8e24" />

![IMG_0376](https://github.com/user-attachments/assets/e1712580-b7e3-4419-8d92-77a83c5f5132)

![IMG_0377](https://github.com/user-attachments/assets/9d45b38a-7960-4284-918c-0cd47c1c77b8)

- Google Wifi mesh with wireless backhaul
- Little visibility into actual performance

<img width="1206" height="2622" alt="IMG_0387" src="https://github.com/user-attachments/assets/73cb46a2-6eef-40d4-9c74-ab24b3c30a3c" />
<img width="1206" height="2622" alt="IMG_0386" src="https://github.com/user-attachments/assets/fc3cbb0e-81a8-4449-8364-0e6b05ed8e73" />
<img width="1206" height="2622" alt="IMG_0385" src="https://github.com/user-attachments/assets/d7f127f7-4caa-4e3b-bac2-ee1da05257d3" />


### How could it be better?
- Wired backhaul
- Out of band performance metrics

### Constraints
- I don't really want to drag ethernet through the house

---

## 2. The MoCA Solution (3 minutes)

![IMG_0389](https://github.com/user-attachments/assets/8ed02ddd-d17c-43c1-877e-c8bd9e594200)


### What is MoCA?
- **Multimedia over Coax Alliance** - Ethernet over existing cable TV wiring
- Transforms dead coax into gigabit network backbone
- Google Wifi gets wired backhaul without new cables

![IMG_0391](https://github.com/user-attachments/assets/1d705d5d-33dd-47ea-8b5e-5447a0f86c4d)

<img width="342" height="472" alt="network-2 drawio" src="https://github.com/user-attachments/assets/4e436187-faff-4bed-b5dc-c5ad52fab0c7" />

### Results
- **Before**: Probably fine
- **After**: Wired backbone, arguably better
- *But now there's a problem...*

---

## 3. What Not to Do: ISP Truck Roll Stories (3 minutes)

### Mistake #1: Don't split the streams
- Installed splitter
- Created signal degradation
- ISP tech: *"Why did you do this?"*

### Key Lesson
- Don't use too many splitters.
- Gee it would have been cool to have the Modem data for all these *before* I called.

<img width="889" height="589" alt="Screenshot 2025-10-13 at 13 20 56" src="https://github.com/user-attachments/assets/fbb56b0a-cf66-40a1-9211-95cfb647ff79" />

### Disappoint
- Don't want to waste all this coax and MoCa devices.
- Don't want to go back to wireless backhaul for the mesh.
- Sad panda.

---

## 4. Re-architect to keep the MoCa part

### Move things around
- Keep MoCa
- Keep wired backhaul
- Route around splitter limitation that causes problems

<img width="342" height="452" alt="network-3 drawio" src="https://github.com/user-attachments/assets/d4e39833-c78d-41f7-a553-5de39ebc874f" />

![IMG_0393](https://github.com/user-attachments/assets/0c06194c-9dcc-4ed0-a66f-90c4547f7967)


## 5. Scope Creep: The Monitoring Rabbit Hole (4 minutes)

### The Evolution
```
"Let me check modem status occasionally"
"I should automate this HTML parsing" 
"Maybe store it in InfluxDB"
"Grafana would make nice dashboards"
"Kubernetes isn't overkill... right?"
"I don't want to write this code."
"Maybe getting PurpleAir and GoogleWifi data would be easier since it's JSON."
```

### PurpleAir has some nice data to graph
You can hit it on an HTTP endpoint inside your network.

`http://192.168.86.250/json?live=true`

```
{
  "SensorId": "68:c6:3a:ff:87:6b",
  "DateTime": "2025/10/09T21:40:36z",
  "Geo": "PurpleAir-876b",
  "Mem": 17200,
  "memfrag": 10,
  "memfb": 15552,
  "memcs": 928,
  "Id": 52879,
  "lat": 44.1017,
  "lon": -121.2855,
  "Adc": 0.02,
  "loggingrate": 15,
  "place": "outside",
  "version": "7.02",
  "uptime": 585443,
  "rssi": -58,
  "period": 120,
  "httpsuccess": 5039,
  "httpsends": 9917,
  "hardwareversion": "2.0",
  "hardwarediscovered": "2.0+BME280+PMSX003-B+PMSX003-A",
  "current_temp_f": 70,
  "current_humidity": 40,
  "current_dewpoint_f": 45,
  "pressure": 892.68,
  "p25aqic_b": "rgb(112,240,0)",
  "pm2.5_aqi_b": 38,
  "pm1_0_cf_1_b": 7,
  "p_0_3_um_b": 1518,
  "pm2_5_cf_1_b": 9,
  "p_0_5_um_b": 404,
  "pm10_0_cf_1_b": 9,
  "p_1_0_um_b": 48,
  "pm1_0_atm_b": 7,
  "p_2_5_um_b": 2,
  "pm2_5_atm_b": 9,
  "p_5_0_um_b": 0,
  "pm10_0_atm_b": 9,
  "p_10_0_um_b": 0,
  "p25aqic": "rgb(50,233,0)",
  "pm2.5_aqi": 29,
  "pm1_0_cf_1": 7,
  "p_0_3_um": 1527,
  "pm2_5_cf_1": 7,
  "p_0_5_um": 388,
  "pm10_0_cf_1": 7,
  "p_1_0_um": 40,
  "pm1_0_atm": 7,
  "p_2_5_um": 0,
  "pm2_5_atm": 7,
  "p_5_0_um": 0,
  "pm10_0_atm": 7,
  "p_10_0_um": 0,
  "pa_latency": 554,
  "response": -11,
  "response_date": 1760045970,
  "latency": 597,
  "wlstate": "Connected",
  "status_0": 2,
  "status_1": 2,
  "status_2": 2,
  "status_3": 2,
  "status_4": 0,
  "status_5": 0,
  "status_6": 3,
  "status_7": 0,
  "status_8": 0,
  "status_9": 0,
  "ssid": "NachoWIFI"
}
```

PA has good docs on what each means: https://community.purpleair.com/t/sensor-json-documentation/6917

![pa_dash-1](https://github.com/user-attachments/assets/32b86b3c-ab78-4a0f-a007-7f82f1e5da0f)
![pa_dash-2](https://github.com/user-attachments/assets/a3ca79a2-743e-44ea-8bc6-052a61b0eb72)

### Google Wifi less so

`http://192.168.86.32/api/v1/status`

```
{
   "dns": {
      "mode": "automatic",
      "servers": [  ]
   },
   "setupState": "GWIFI_OOBE_COMPLETE",
   "software": {
      "blockingUpdate": 1,
      "softwareVersion": "14150.376.32",
      "updateChannel": "stable-channel",
      "updateNewVersion": "0.0.0.0",
      "updateProgress": 0.0,
      "updateRequired": false,
      "updateStatus": "idle"
   },
   "system": {
      "countryCode": "us",
      "groupRole": "leaf",
      "hardwareId": "GALE C2I-A2A-A3C-A4I-E87",
      "lan0Link": true,
      "ledAnimation": "CONNECTED",
      "ledIntensity": 0,
      "modelId": "ACc3d",
      "oobeDetailedStatus": "INITIALIZATION_STAGE_DEVICE_ONLINE",
      "uptime": 5861923
   },
   "vorlonInfo": {
      "migrationMode": "vorlon_all"
   },
   "wan": {
      "captivePortal": false,
      "ethernetLink": false,
      "gatewayIpAddress": "192.168.86.1",
      "invalidCredentials": false,
      "ipAddress": true,
      "ipMethod": "dhcp",
      "ipPrefixLength": 24,
      "leaseDurationSeconds": 86400,
      "localIpAddress": "192.168.86.32",
      "nameServers": [  ],
      "online": true,
      "pppoeDetected": false,
      "vlanScanAttemptCount": 0,
      "vlanScanComplete": true
   }
}
```
![Screenshot from 2025-07-06 14-48-07](https://github.com/user-attachments/assets/385af34e-9c31-4ad7-ab29-b3a44f469209)
![Screenshot from 2025-07-06 14-48-36](https://github.com/user-attachments/assets/e5f34aac-64b8-42a1-afe8-8f6126c7a3b3)

### Arris modem has a lot of data
- `http://192.168.100.1/cmswinfo.htm`
- `http://192.168.100.1/cmconnectionstatus.html`
- But it's not easy to parse
- There are several existing projects, but none of them just work
- I really don't want to dig into this code to figure out why the HTML won't parse.
- This does not spark joy

### Enter AI as Coding Copilot
- **Claude**: "Help me parse this ugly HTML"
- AI handled boilerplate, human provided architecture
- Rapid prototyping of Python parser
- https://github.com/augieschwer/home-networking-monitoring/blob/dev/src/parse_modem_status.py
- Even wrote documentation!
- https://github.com/augieschwer/home-networking-monitoring/blob/dev/README.md#cable-modem-status-parser

### The Final Stack
- **Kubernetes** + **InfluxDB** + **Telegraf** + **Grafana**
- Custom Python scripts parsing cable modem HTML
- NOC-style dashboards for home network
- *Definitely overkill, absolutely worth it*, probably.

---

## 6. The NOC Dashboard (2 minutes)

### Professional Home Monitoring
- **Real-time Status**: Visual connection health
- **Signal Heatmaps**: Per-channel performance
- **Historical Trends**: Error rates and quality over time
- Google Wifi data

### Home Air Quality Monitoring
- Trends over time for AQI
- Temperature
- Humidity

---

## 7. Was This All Overkill? (2 minutes)

### Honest Answer: Yes... But
- **Overkill**: Definitely more complex than needed
- **Learning**: Real K8s skills for home projects
- **Reproducible**: Helm charts for everything
- **Shareable**: Easy to document and replicate
- Chance to see how well the robot could write and document code.
- Some times we do things just because we can.

---

## 8. Lessons Learned & Should You Do This? (1 minute)

### Do This If You:
- Enjoy the journey more than destination
- Want to learn modern monitoring tools
- Have time for "unnecessary" optimization
- Need impressive dashboards to show off
- Want access to the data on your network without having to leave your network

### Skip This If You:
- "Good enough" actually is good enough
- Don't want to become your own network admin
- Value simplicity over visibility
- *Your family already questions your tech projects*

### Final Wisdom
*"The best network monitoring is the one you actually use. The second-best is the unnecessarily complicated one that teaches you Kubernetes."*

---

## Q&A & Live Demo
**Want to see the dashboards in action?**

*Repository: github.com/augieschwer/home-networking-monitoring*
