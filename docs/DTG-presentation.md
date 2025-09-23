# My Overly Complicated Home Networking and Monitoring Project
**A 20-Minute Journey from "Wired backhaul" to Full NOC style monitoring and metrics**

*Featuring MoCA magic, AI coding assistance, and hard-learned lessons about ISP truck rolls*

---

## 1. The Problem (2 minutes)

### The Setup That "Worked Fine"
- Google Wifi mesh with wireless backhaul
- Zero visibility into actual performance

### The Constraint
- Existing unused coax throughout house
- Challenge: Better network without drilling holes

---

## 2. The MoCA Solution (3 minutes)

### What is MoCA?
- **Multimedia over Coax Alliance** - Ethernet over existing cable TV wiring
- Transforms dead coax into gigabit network backbone
- Google Wifi gets wired backhaul without new cables

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

## 5. Scope Creep: The Monitoring Rabbit Hole (4 minutes)

### Week-by-Week Evolution
```
Week 1: "Let me check modem status occasionally"
Week 2: "I should automate this HTML parsing" 
Week 3: "Maybe store it in InfluxDB"
Week 4: "Grafana would make nice dashboards"
Week 5: "Kubernetes isn't overkill... right?"
I don't want to write this code.
Maybe getting PurpleAir and GoogleWifi data would be easier since it's JSON.
```

### PurpleAir has some nice data to graph

### Google Wifi less so

### Arris modem has a lot of data
- But it's not easy to parse
- There are several existing projects, but none of them just work
- I really don't want to dig into this code to figure out why the HTML won't parse.

### Enter AI as Coding Copilot
- **Claude**: "Help me parse this ugly HTML"
- AI handled boilerplate, human provided architecture
- Rapid prototyping of Python parser
- Even wrote documentation!

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
