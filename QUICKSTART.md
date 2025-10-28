# 🚀 Quick Start Guide - ARP Spoofing Simulation

## Fastest Way to Get Started (60 seconds)

### Option 1: Interactive Launcher (Recommended)
```powershell
python run_demo.py
```
Then select option 1 for basic simulation!

### Option 2: Direct Launch
```powershell
# Install dependencies
pip install matplotlib

# Run basic simulation
python arp_sim.py
```

---

## What to Expect

### Timeline of Events

**Seconds 0-3**: Initial State
- Window opens with three network nodes
- Victim's ARP cache is empty
- Gray line (no connectivity)

**Seconds 3-6**: Normal ARP
- Victim sends ARP request
- Gateway replies with correct MAC
- Cache updated, line turns **GREEN** ✅

**Seconds 6+**: Attack Begins
- Spoofer sends forged ARP replies
- Victim's cache gets poisoned
- Line turns **RED** ⚠️ (MITM active!)

---

## Basic Controls

| Key | What It Does | When to Use |
|-----|-------------|-------------|
| **r** | Send correct ARP (repair) | When you see red line |
| **s** | Enable static ARP (lock mapping) | To prevent further poisoning |
| **q** | Quit simulation | When done |

---

## 2-Minute Demo Script

**Perfect for presentations or quick understanding:**

1. **Start**: `python arp_sim.py`
2. **Wait 5 seconds**: Watch the flow go from gray → green
3. **Wait 5 more seconds**: Watch it turn red (attack!)
4. **Press 'r'**: See it go green again (but temporarily)
5. **Press 's'**: Victim node turns light green (protected!)
6. **Explain**: "This is how ARP poisoning works and how we defend against it"

---

## Common Questions

**Q: Is this safe?**  
A: Yes! 100% safe. No real network packets, no root needed, no risk.

**Q: What if I don't see colors?**  
A: Check that matplotlib is installed and your display supports colors.

**Q: Can I slow it down?**  
A: Yes! Edit `arp_sim.py`, lines 11-13, increase the time values.

**Q: What am I learning?**  
A: How ARP maps IP→MAC, how attacks work, and why defenses matter.

---

## Next Steps

### For Presentations
→ Read [DEMO_GUIDE.md](./DEMO_GUIDE.md) for detailed scenarios

### For Deep Learning
→ Read [THEORY.md](./THEORY.md) for protocol details

### For Advanced Features
→ Run `python arp_sim_extended.py` for detection & logging

### For Reports/Assignments
→ Use the extended version and export statistics with 'e' key

---

## Troubleshooting

**Problem**: "matplotlib not found"  
**Solution**: `pip install matplotlib`

**Problem**: Window opens but is blank  
**Solution**: Add this at line 6 of arp_sim.py:
```python
import matplotlib
matplotlib.use('TkAgg')
```

**Problem**: Can't see what's happening  
**Solution**: Check the console/terminal - events are logged there too!

---

## File Guide

| File | Purpose | When to Use |
|------|---------|-------------|
| `run_demo.py` | Interactive menu | First time, demos |
| `arp_sim.py` | Basic simulation | Quick demonstrations |
| `arp_sim_extended.py` | Advanced features | Research, reports |
| `README.md` | Full documentation | Reference, overview |
| `DEMO_GUIDE.md` | Presentation scripts | Teaching, presenting |
| `THEORY.md` | Technical deep dive | Learning, studying |

---

**Ready to Start?**

```powershell
python run_demo.py
```

or

```powershell
python arp_sim.py
```

**Have fun learning! Stay ethical! 🔐**
