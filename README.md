# ARP Spoofing Simulation & Learning Tool 🔒

A **safe, educational simulation** of ARP spoofing attacks and defenses. No root privileges, no real network packets, no risk. Perfect for computer networks courses and cybersecurity education.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-Educational-green.svg)
![Safe](https://img.shields.io/badge/Safe-No%20Real%20Network%20Traffic-brightgreen.svg)

---

## 🎯 What This Project Demonstrates

This simulation illustrates:

- ✅ **ARP Protocol Behavior**: How IP-to-MAC address resolution works at the data-link layer
- ✅ **ARP Cache Poisoning**: Man-in-the-Middle (MITM) attack technique
- ✅ **Attack Visualization**: Real-time visual representation with color-coded traffic flow
- ✅ **Defense Mechanisms**: Gratuitous ARP and static ARP entries
- ✅ **Network Security Concepts**: Applied learning for Unit I & III of Computer Networks syllabus

### Visual Indicators

| Color | Meaning |
|-------|---------|
| 🟢 **Green** | Legitimate traffic flow (correct ARP mapping) |
| 🔴 **Red** | Poisoned traffic flow (victim sending packets to attacker) |
| ⚪ **Gray** | No ARP mapping yet (cache empty) |

---

## 🚀 Quick Start (30 seconds)

### Prerequisites

- Python 3.7 or higher
- `matplotlib` library

### Installation

```powershell
# Clone or navigate to project directory
cd d:\Projects\CN-demo

# Install dependencies
pip install matplotlib

# Run the simulation
python arp_sim.py
```

That's it! The simulation window will open automatically.

---

## 📖 How to Use

### Basic Controls

| Key | Action | Description |
|-----|--------|-------------|
| **r** | Send Gratuitous ARP | Restores correct ARP mapping (defense) |
| **s** | Toggle Static ARP | Enable/disable static ARP entries (prevents updates) |
| **q** | Quit | Close the simulation |

### What You'll See

1. **Three Network Nodes**:
   - 🔵 **Victim** (192.168.1.10) - The target host
   - 🟢 **Gateway** (192.168.1.1) - Legitimate router
   - 🔴 **Spoofer** (192.168.1.80) - Attacker performing ARP spoofing

2. **ARP Cache Display**: Shows the victim's current IP→MAC mappings in real-time

3. **Event Log**: Console and on-screen log showing ARP requests, replies, and attacks

4. **Visual Traffic Flow**: Line connecting Victim to Gateway changes color based on ARP cache state

---

## 🎓 Demo Script (2-3 Minutes)

### Step 1: Initial State (0-3 seconds)
- **Observe**: Victim's ARP cache is empty
- **Flow**: Gray line (no connectivity)
- **Explain**: "Without ARP mapping, the victim can't communicate with the gateway"

### Step 2: Legitimate ARP Exchange (3-6 seconds)
- **Event**: Victim sends ARP Request for gateway IP
- **Response**: Gateway replies with correct MAC address
- **Result**: ARP cache populated, flow turns **green**
- **Explain**: "Normal ARP: Victim learns Gateway IP → Gateway MAC"

### Step 3: ARP Spoofing Attack (6-10 seconds)
- **Event**: Spoofer sends forged ARP replies
- **Claim**: "Gateway IP is at Spoofer MAC" (fake!)
- **Result**: ARP cache updated, flow turns **red**
- **Explain**: "ARP poisoning: Victim now sends gateway traffic to attacker"

### Step 4: Defense Demonstration (Press 'r')
- **Action**: Send gratuitous ARP from gateway
- **Result**: Cache restored, flow returns to **green**
- **Explain**: "Gratuitous ARP repair: Gateway reasserts correct mapping"

### Step 5: Static ARP Defense (Press 's')
- **Action**: Enable static ARP entries
- **Result**: Victim node turns light green, ignores further poisoning
- **Explain**: "Static ARP: Mapping locked, immune to forged replies"

---

## 📚 Educational Mapping

### Computer Networks Syllabus Coverage

#### **Unit I: Data Link Layer**
- Address Resolution Protocol (ARP)
- MAC address vs IP address
- Frame forwarding and switching
- Address mapping mechanisms

#### **Unit III: Network Layer**
- IP addressing and subnetting
- Address translation between layers
- Network security fundamentals

#### **Security Extension** (Beyond Basic Syllabus)
- Man-in-the-Middle (MITM) attacks
- ARP cache poisoning techniques
- Network security defenses
- Attack detection and mitigation

---

## 🔬 Technical Deep Dive

### How ARP Works (Normal Operation)

```
1. Victim needs to send IP packet to 192.168.1.1
2. Victim checks ARP cache: Empty!
3. Victim broadcasts: "Who has 192.168.1.1? Tell 192.168.1.10"
4. Gateway responds: "192.168.1.1 is at GG:GG:GG:GG:GG:01"
5. Victim caches: 192.168.1.1 → GG:GG:GG:GG:GG:01
6. Victim sends Ethernet frame to Gateway's MAC
```

### How ARP Spoofing Works (Attack)

```
1. Spoofer monitors network traffic
2. Spoofer sends forged ARP reply to Victim:
   "192.168.1.1 is at SS:SS:SS:SS:SS:80" (LIE!)
3. Victim updates cache: 192.168.1.1 → SS:SS:SS:SS:SS:80
4. Victim now sends Gateway-bound frames to Spoofer
5. Spoofer can intercept, modify, or drop packets (MITM)
```

### Why ARP is Vulnerable

- ❌ **No authentication**: ARP has no built-in security
- ❌ **Stateless protocol**: Hosts accept unsolicited ARP replies
- ❌ **Trust model**: Assumes all nodes on LAN are trustworthy
- ❌ **Broadcast nature**: All hosts can see ARP traffic

---

## 🛡️ Defense Mechanisms Explained

### 1. Gratuitous ARP (Reactive)
**What it is**: A host broadcasts ARP reply about its own IP address

**How to use in simulation**: Press **'r'** key

**Pros**:
- ✅ Quick to restore correct mapping
- ✅ No configuration required
- ✅ Works immediately

**Cons**:
- ❌ Temporary fix (attacker can re-poison)
- ❌ Reactive, not preventive
- ❌ Race condition with attacker

**Real-world use**: Network admins can send gratuitous ARP when detecting attacks

### 2. Static ARP Entries (Preventive)
**What it is**: Manually configuring IP→MAC mappings that don't change

**How to use in simulation**: Press **'s'** key

**Pros**:
- ✅ Immune to ARP poisoning
- ✅ Persistent protection
- ✅ No race conditions

**Cons**:
- ❌ Doesn't scale to large networks
- ❌ Manual maintenance required
- ❌ Breaks when hardware changes

**Real-world command**:
```bash
# Linux
arp -s 192.168.1.1 GG:GG:GG:GG:GG:01

# Windows
arp -s 192.168.1.1 GG-GG-GG-GG-GG-01
```

### 3. Production Defenses (Not in simulation, for reference)

#### Dynamic ARP Inspection (DAI)
- Switch feature that validates ARP packets
- Checks against DHCP snooping database
- Drops invalid/suspicious ARP replies

#### Port Security
- Limits which MAC addresses can connect to switch ports
- Prevents unauthorized devices from spoofing

#### 802.1X Network Access Control
- Authentication before network access granted
- Ensures only authorized devices on network

---

## 🎬 Demo Scenarios for Presentations

### Scenario 1: "The Attack"
**Purpose**: Show how ARP poisoning works

1. Run simulation, wait for green flow
2. Point out legitimate ARP cache entry
3. Watch spoofer inject forged replies
4. **Emphasize**: Cache changed, flow now red
5. **Explain**: "All gateway traffic now goes through attacker"

**Time**: 30 seconds

### Scenario 2: "The Defense"
**Purpose**: Demonstrate mitigation techniques

1. Show poisoned state (red flow)
2. Press 'r' → Gratuitous ARP repair
3. Note: Attacker can re-poison (show this happening)
4. Press 's' → Static ARP enabled
5. **Emphasize**: Now immune to further attacks
6. **Explain**: Trade-off between security and flexibility

**Time**: 45 seconds

### Scenario 3: "Real-World Impact"
**Purpose**: Connect simulation to actual threats

1. Show attack in action
2. Explain what attacker could do:
   - Steal passwords (HTTP traffic)
   - Hijack sessions (cookies)
   - Inject malicious content
   - Perform denial-of-service
3. Discuss why HTTPS is important (encrypted payload)
4. Note: ARP poisoning still allows traffic analysis

**Time**: 60 seconds

---

## 🧪 Extending the Simulation

See `arp_sim_extended.py` for advanced features:

- 🔍 **Attack Detection**: Heuristics to detect ARP poisoning
- 📊 **Statistics Dashboard**: Packet counts and attack metrics
- 💾 **Log Export**: Save events to file for reports
- 📦 **Packet Payloads**: Visualize intercepted "data"
- 🎯 **Multiple Victims**: Simulate larger network

### Quick Extensions You Can Add

#### 1. Detection Alert (10 minutes)
```python
# Add to process_arp_reply function
if prev is not None and prev != mac:
    alert = f"⚠️ WARNING: ARP mapping changed for {ip}"
    alert += f"\n  Old: {prev}\n  New: {mac}"
    log(alert)
```

#### 2. Export Log (5 minutes)
```python
# Add button handler
elif event.key == 'e':
    with open('arp_log.txt', 'w') as f:
        f.write('\n'.join(LOG_LINES))
    log("Exported log to arp_log.txt")
```

#### 3. Packet Counter (10 minutes)
```python
# Add global counters
legitimate_packets = 0
forged_packets = 0

# Update in send_arp_reply / send_forged_reply
# Display in matplotlib text box
```

---

## 🎓 For Instructors & Students

### Discussion Questions

1. **Protocol Design**: Why doesn't ARP include authentication? What would be the cost?

2. **Trust Models**: What assumptions does ARP make about network participants?

3. **Layer Interactions**: How does ARP bridge the network layer (IP) and data-link layer (MAC)?

4. **Security vs Usability**: Why aren't static ARP entries used everywhere?

5. **Modern Solutions**: How do switches with DAI improve on host-based defenses?

### Lab Exercise Ideas

1. **Timing Analysis**: Modify intervals and observe when attacks succeed/fail

2. **Detection Algorithm**: Implement heuristic to detect ARP spoofing

3. **Network Topology**: Extend to 5+ nodes, multiple attackers

4. **Defense Comparison**: Measure effectiveness of different mitigation strategies

5. **Real-World Mapping**: Map simulation to actual network hardware/software

### Report/Assignment Suggestions

1. Run simulation, take screenshots of each phase
2. Explain ARP protocol operation (with packet format)
3. Describe attack mechanism and MITM threat model
4. Compare defense mechanisms (table of pros/cons)
5. Research production solutions (DAI, port security)
6. Include code snippets showing key functions

---

## 📂 Project Structure

```
CN-demo/
├── arp_sim.py              # Main simulation (this file)
├── arp_sim_extended.py     # Advanced features demo
├── run_demo.py             # Quick-start script with guided tour
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── DEMO_GUIDE.md          # Detailed walkthrough scenarios
├── THEORY.md              # Deep dive into ARP and attacks
└── screenshots/           # Demo images (optional)
```

---

## ⚠️ Important Notes

### This is a SIMULATION
- **No real network packets** are sent
- **No administrator privileges** required
- **No actual security risk** to your network
- Safe for classroom, lab, and personal use

### Educational Use Only
This tool is designed for:
- ✅ Computer Networks courses
- ✅ Cybersecurity education
- ✅ Protocol understanding
- ✅ Defense awareness

**NOT for**:
- ❌ Actual network attacks
- ❌ Unauthorized access
- ❌ Malicious purposes

### Legal & Ethical
- Only use on your own systems or with explicit permission
- Understand that real ARP spoofing is illegal in most jurisdictions
- This simulation is provided for educational purposes only

---

## 🤝 Contributing

Ideas for improvements:
- Add more defense mechanisms (ARP monitoring tools)
- Create interactive quiz mode
- Add network capture/replay from pcap files
- Implement more sophisticated detection algorithms
- Create video tutorials

---

## 📞 Support & Resources

### Quick Links
- [DEMO_GUIDE.md](./DEMO_GUIDE.md) - Step-by-step walkthrough
- [THEORY.md](./THEORY.md) - In-depth ARP explanation
- [Python matplotlib docs](https://matplotlib.org/stable/contents.html)

### Troubleshooting

**Issue**: Simulation window doesn't open
- **Fix**: Ensure matplotlib is installed: `pip install matplotlib`

**Issue**: Animation is slow/laggy
- **Fix**: Increase `FRAME_INTERVAL_MS` in code (line 14)

**Issue**: Can't see the plot on Windows
- **Fix**: Try different matplotlib backend: `import matplotlib; matplotlib.use('TkAgg')`

---

## 📄 License

**Educational Use License**

This project is provided for educational purposes. You are free to:
- Use it in academic settings
- Modify it for learning
- Share it with students/colleagues

Please maintain attribution and educational context.

---

## 🌟 Acknowledgments

Designed for Computer Networks & Cybersecurity education.  
Special thanks to the matplotlib and Python communities.

---

**Made with ❤️ for learning and education**

*Version 1.0 - Safe, Simple, Educational*
