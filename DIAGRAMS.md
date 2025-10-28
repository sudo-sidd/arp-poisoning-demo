# Visual Diagrams for ARP Spoofing

## Network Topology Diagram

```
         Normal ARP Operation
         ====================

    ┌─────────────┐
    │   Victim    │ 192.168.1.10
    │ (Computer)  │ MAC: AA:...10
    └──────┬──────┘
           │
           │ 1. "Who has 192.168.1.1?"
           │    (ARP Request - Broadcast)
           ↓
    ═══════════════════════════════
           LAN (Ethernet)
    ═══════════════════════════════
           ↓
           │ 2. "192.168.1.1 is at GG:...01"
           │    (ARP Reply - Unicast)
    ┌──────┴──────┐
    │   Gateway   │ 192.168.1.1
    │   (Router)  │ MAC: GG:...01
    └─────────────┘
```

---

## ARP Spoofing Attack Diagram

```
         ARP Poisoning Attack
         ====================

    ┌─────────────┐
    │   Victim    │ 192.168.1.10
    │             │ ARP Cache:
    │             │ 192.168.1.1 → SS:...80 ✗ WRONG!
    └──────┬──────┘
           │
           │ All gateway traffic
           │ goes to attacker!
           ↓
    ┌─────────────┐      ═══════════════════════════════
    │   Spoofer   │             LAN (Ethernet)
    │  (Attacker) │      ═══════════════════════════════
    │             │
    │ 192.168.1.80│           ↑
    │ MAC: SS:...80│           │
    └──────┬──────┘           │
           │                   │
           │ 3. Forged reply   │
           │ "192.168.1.1      │
           │  is at SS:...80"  │
           │                   │
           └───────────────────┘
                               │
                               │ (Optionally forwards
                               │  to real gateway)
                               ↓
                        ┌─────────────┐
                        │   Gateway   │ 192.168.1.1
                        │   (Router)  │ MAC: GG:...01
                        └─────────────┘
```

---

## ARP Cache States Diagram

```
         Victim's ARP Cache Timeline
         ============================

TIME: 0s (Initial State)
┌─────────────────────────────┐
│    ARP Cache: EMPTY         │
│                             │
│  No mappings                │
└─────────────────────────────┘
Status: Cannot communicate (GRAY)


TIME: 3s (After Legitimate ARP)
┌─────────────────────────────┐
│    ARP Cache: VALID         │
│                             │
│  192.168.1.1 → GG:...01 ✓  │
└─────────────────────────────┘
Status: Normal operation (GREEN)


TIME: 6s (After ARP Spoofing)
┌─────────────────────────────┐
│    ARP Cache: POISONED      │
│                             │
│  192.168.1.1 → SS:...80 ✗  │
└─────────────────────────────┘
Status: MITM attack active (RED)


TIME: 10s (After Gratuitous ARP)
┌─────────────────────────────┐
│    ARP Cache: RESTORED      │
│                             │
│  192.168.1.1 → GG:...01 ✓  │
└─────────────────────────────┘
Status: Temporarily fixed (GREEN)


TIME: 15s (Static ARP Enabled)
┌─────────────────────────────┐
│  ARP Cache: LOCKED 🔒       │
│                             │
│  192.168.1.1 → GG:...01 ✓  │
│  (Ignores updates)          │
└─────────────────────────────┘
Status: Protected (GREEN)
```

---

## OSI Layer Interaction

```
         How ARP Bridges Layers
         ======================

Application     HTTP, FTP, DNS
Layer 7         "Send email to mail.example.com"
                |
                ↓
Transport       TCP, UDP
Layer 4         Segment with ports
                |
                ↓
Network         IP
Layer 3         "Send to 192.168.1.1"
                |
                | What MAC address?
                | Need ARP! ───────────┐
                ↓                      │
Data Link       Ethernet               │
Layer 2         "Send to ??:??:??:??" ←┘
                |                      
                | ARP provides:       
                | GG:GG:GG:GG:GG:01   
                ↓                      
Physical        Cables, WiFi
Layer 1         Electrical signals
```

---

## Attack Flow Diagram

```
         Complete Attack Sequence
         ========================

┌─────────┐     ┌─────────┐     ┌─────────┐
│ Victim  │     │ Spoofer │     │ Gateway │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     │ ARP Request   │               │
     │ "Who has .1?" │               │
     ├───────────────┼───────────────►
     │               │               │
     │               │    ARP Reply  │
     │               │ ".1 = GG:01"  │
     ◄───────────────┼───────────────┤
     │               │               │
     │ [Cache: .1→GG:01] ✓          │
     │               │               │
     │        FORGED ARP Reply       │
     │        ".1 = SS:80" (LIE!)    │
     ◄───────────────┤               │
     │               │               │
     │ [Cache: .1→SS:80] ✗ POISONED │
     │               │               │
     │ Send packet   │               │
     │ (to gateway)  │               │
     ├──────────────►│               │
     │               │               │
     │               │ [Intercept!]  │
     │               │ [Read/Modify] │
     │               │               │
     │               │ Forward to    │
     │               │ real gateway  │
     │               ├──────────────►│
     │               │               │
```

---

## Defense Mechanisms Comparison

```
         Static ARP vs Dynamic ARP Inspection
         =====================================

┌─────────────────────────────────────────────┐
│           Static ARP (Host-based)           │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────┐                                │
│  │ Victim  │                                │
│  │         │  Static mapping:               │
│  │  ARP    │  192.168.1.1 → GG:...01       │
│  │ Cache   │  (Locked 🔒)                   │
│  │ (LOCKED)│                                │
│  └─────────┘                                │
│      ↓                                      │
│  Ignores all                                │
│  ARP updates                                │
│                                             │
│  ✓ Simple                                   │
│  ✗ Doesn't scale                            │
└─────────────────────────────────────────────┘


┌─────────────────────────────────────────────┐
│      Dynamic ARP Inspection (Switch)        │
├─────────────────────────────────────────────┤
│                                             │
│         ┌──────────────────┐               │
│         │   Network Switch │               │
│         │                  │               │
│         │  ┌────────────┐  │               │
│         │  │DHCP Snoop  │  │               │
│         │  │ Database   │  │               │
│         │  │.10→AA:10   │  │               │
│         │  │.1 →GG:01   │  │               │
│         │  └────────────┘  │               │
│         │         ↕         │               │
│         │  ┌────────────┐  │               │
│         │  │    DAI     │  │               │
│         │  │ Validation │  │               │
│         │  └────────────┘  │               │
│         └────┬────┬────┬───┘               │
│              │    │    │                    │
│          ┌───┘    │    └───┐               │
│      Victim    Spoofer   Gateway           │
│                                             │
│  Forged ARP → DROPPED by switch            │
│                                             │
│  ✓ Scales well                              │
│  ✗ Requires managed switches                │
└─────────────────────────────────────────────┘
```

---

## Man-in-the-Middle Visualization

```
         Before Attack (Normal)
         ======================

    ┌─────────┐                    ┌─────────┐
    │ Victim  │ ──────────────────► │ Gateway │
    │         │    Direct path      │         │
    │         │ ◄────────────────── │         │
    └─────────┘                    └─────────┘
                                        │
                                        │
                                        ↓
                                   Internet


         After ARP Poisoning
         ===================

    ┌─────────┐      ┌───────────┐      ┌─────────┐
    │ Victim  │ ────►│  Spoofer  │─────►│ Gateway │
    │         │      │ (Attacker)│      │         │
    │         │ ◄────│           │◄─────│         │
    └─────────┘      │  Reads/   │      └─────────┘
                     │ Modifies  │           │
                     │  Traffic  │           │
                     └───────────┘           ↓
                           │            Internet
                           │
                           ↓
                     Stolen Data,
                     Passwords,
                     Session Cookies
```

---

## Simulation Color Code

```
         Visual Status Indicators
         ========================

    GRAY Line (──────)
    ├─ Meaning: No ARP mapping
    ├─ Victim state: Cannot communicate
    └─ Action needed: Wait for ARP exchange


    GREEN Line (──────)
    ├─ Meaning: Correct ARP mapping
    ├─ Victim state: Normal operation
    └─ Security: SAFE ✓


    RED Line (──────)
    ├─ Meaning: Poisoned ARP cache
    ├─ Victim state: MITM attack active
    └─ Security: COMPROMISED ✗


    Node Colors:
    ┌──────────────────────────────────────┐
    │ 🔵 Blue (Light)   = Victim (normal)  │
    │ 🟢 Green (Light)  = Victim (static)  │
    │ 🟢 Green          = Gateway          │
    │ 🔴 Red            = Spoofer/Attacker │
    └──────────────────────────────────────┘
```

---

## Packet Structure Visualization

```
         ARP Packet Structure (28 bytes)
         ================================

Byte:  0  1  2  3  4  5  6  7  8  9 10 11 ...
      ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐
    0 │Hardware Type  │Protocol Type  │HL│PL│
      ├──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┤
    8 │    Operation    │  Sender HW Addr  │
      ├─────────────────┼──────────────────┤
   16 │  (cont'd)       │ Sender Proto Addr│
      ├─────────────────┼──────────────────┤
   24 │Target HW Address│  Target Proto ..  │
      └─────────────────┴──────────────────┘

Legend:
  Hardware Type (2): 0x0001 = Ethernet
  Protocol Type (2): 0x0800 = IPv4
  HL (1): 6 (MAC is 6 bytes)
  PL (1): 4 (IPv4 is 4 bytes)
  Operation (2): 1=Request, 2=Reply
  Sender HW Addr (6): Sender's MAC
  Sender Proto Addr (4): Sender's IP
  Target HW Addr (6): Target's MAC (00:00:00:00:00:00 in request)
  Target Proto Addr (4): Target's IP
```

---

## Timeline Diagram for 2-Minute Demo

```
Time  Event                              Visual        Audio Cue
====  =================================  ============  ===================
0:00  Start simulation                   Gray line     "Starting demo..."

0:05  Victim sends ARP request           Gray line     "Victim asks for
                                                        gateway MAC"

0:06  Gateway replies                    Gray→Green    "Gateway replies"
      Cache learns correct mapping                     "Cache updated!"

0:10  Spoofer sends forged reply         Green→Red     "Attack begins!"
      Cache poisoned                                   "Cache poisoned!"

0:15  Press 'r' - Gratuitous ARP         Red→Green     "Sending repair"

0:20  Re-poisoned by spoofer             Green→Red     "Re-attacked!"

0:22  Press 's' - Enable static ARP      Red→Green     "Enabling defense"
      Victim node turns light green      (stays green) "Now protected!"

0:30  Demo complete                                    "Questions?"
```

---

## Detection Heuristics Flowchart

```
         ARP Anomaly Detection Logic
         ============================

    New ARP Reply Received
            │
            ↓
    ┌───────────────────┐
    │ IP in cache?      │
    └───┬───────────┬───┘
        │ No        │ Yes
        ↓           ↓
    ┌───────┐   ┌──────────────────┐
    │ Learn │   │ MAC same as old? │
    │ New   │   └───┬──────────┬───┘
    │ Entry │       │ Yes      │ No
    └───────┘       ↓          ↓
                ┌───────┐  ┌──────────────┐
                │ Update│  │ Check timing │
                │ Timer │  └───┬──────────┘
                └───────┘      │
                               ↓
                        ┌──────────────────┐
                        │ Changed within   │
                        │ last 60 seconds? │
                        └───┬──────────┬───┘
                            │ No       │ Yes
                            ↓          ↓
                        ┌───────┐  ┌───────────┐
                        │ Normal│  │ 🚨 ALERT  │
                        │ Update│  │ Possible  │
                        └───────┘  │ Spoofing! │
                                   └───────────┘
```

---

**These diagrams complement the simulation and documentation.**  
**Print them out for presentations or include in reports!**
