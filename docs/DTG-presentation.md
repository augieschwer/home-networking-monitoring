# My Overly Complicated Home Networking and Monitoring Project
**A 20-Minute Journey from "Just Some Basic Metrics" to Full NOC Insanity**

*Featuring MoCA magic, AI coding assistance, and hard-learned lessons about ISP truck rolls*

---

## 1. The Problem (2 minutes)

### The Setup That "Worked Fine"
- Google Wifi mesh with wireless backhaul
- Mysterious slowdowns and dropouts
- Zero visibility into actual performance
- *"I just want to see some metrics..."*

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

---

## 4. Scope Creep: The Monitoring Rabbit Hole (4 minutes)

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

## 5. The Cable Modem Data Goldmine (3 minutes)

### Arris SB8200 Hidden Metrics
- HTML status pages with 32+ channel details
- Signal quality, power levels, error rates per channel
- Real-time bonding and performance data

### Custom Python Parser + AI
```python
# What AI helped build:
def parse_modem_status():
    # Fetch from /cmswinfo.html and /cmconnectionstatus.html
    # Parse ugly HTML tables (thanks, Beautiful Soup)
    # Convert to InfluxDB line protocol
    # Handle edge cases AI found
```

### Metrics That Actually Matter
- **Channel Bonding**: 32 downstream locked vs total
- **Signal Quality**: SNR >30dB, power 7-10 dBmV  
- **Error Rates**: Correctable vs uncorrectable trends
- **Performance**: Real vs theoretical speeds

---

## 6. The NOC Dashboard (2 minutes)

### Professional Home Monitoring
- **Real-time Status**: Visual connection health
- **Signal Heatmaps**: Per-channel performance
- **Historical Trends**: Error rates and quality over time

---

## 7. Was Kubernetes Overkill? (2 minutes)

### Honest Answer: Yes... But
- **Overkill**: Definitely more complex than needed
- **Learning**: Real K8s skills for home projects
- **Reproducible**: Helm charts for everything
- **Shareable**: Easy to document and replicate

### The Trade-off
- More moving parts = more things to break
- But better organization and GitOps workflow
- *Your mileage may vary on complexity tolerance*

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
