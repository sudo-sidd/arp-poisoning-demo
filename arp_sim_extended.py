# arp_sim_extended.py
# Extended ARP spoofing simulation with detection, logging, and statistics
# Requires: Python 3.x and matplotlib
# Run: python arp_sim_extended.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import random
import time
from datetime import datetime

# --- Simulation Parameters ---
ARP_REQUEST_INTERVAL = 3.0
GATEWAY_REPLY_DELAY = 0.4
SPOOFER_INTERVAL = 2.0
FRAME_INTERVAL_MS = 200

# --- Statistics tracking ---
stats = {
    "arp_requests": 0,
    "legitimate_replies": 0,
    "forged_replies": 0,
    "cache_poisonings": 0,
    "detections": 0,
    "restorations": 0
}

# --- Node definitions ---
victim = {
    "name": "Victim",
    "ip": "192.168.1.10",
    "mac": "AA:AA:AA:AA:AA:10",
    "arp": {}
}
gateway = {
    "name": "Gateway",
    "ip": "192.168.1.1",
    "mac": "GG:GG:GG:GG:GG:01"
}
spoofer = {
    "name": "Spoofer",
    "ip": "192.168.1.80",
    "mac": "SS:SS:SS:SS:SS:80"
}

# --- State ---
_last_arp_request = time.time()
_last_spoof = time.time()
static_arp_enabled = False
detection_enabled = True
auto_defend_enabled = False

# --- ARP history for detection ---
arp_history = []  # List of (timestamp, ip, mac, type) tuples

# --- Logging ---
LOG_LINES = []
log_file = None

def log(msg, level="INFO"):
    t = time.strftime("%H:%M:%S")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{t}] [{level}] {msg}"
    LOG_LINES.append(formatted)
    if len(LOG_LINES) > 10:
        LOG_LINES.pop(0)
    print(formatted)
    
    # Write to file if enabled
    if log_file:
        log_file.write(f"{timestamp} {formatted}\n")
        log_file.flush()

def start_logging():
    global log_file
    filename = f"arp_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_file = open(filename, 'w')
    log(f"Started logging to {filename}", "SYSTEM")
    return filename

def stop_logging():
    global log_file
    if log_file:
        log("Stopped logging", "SYSTEM")
        log_file.close()
        log_file = None

# --- Detection system ---
def detect_arp_anomaly(ip, new_mac, event_type):
    """Detect suspicious ARP behavior"""
    if not detection_enabled:
        return False, None
    
    # Check for MAC flip-flop (same IP, different MACs in short time)
    recent = [h for h in arp_history if h[1] == ip and time.time() - h[0] < 60]
    if len(recent) > 0:
        macs = set(h[2] for h in recent)
        if len(macs) > 1 and new_mac not in macs:
            stats["detections"] += 1
            return True, "MAC_FLIP_FLOP"
    
    # Check for too many updates in short time
    if len(recent) > 5:
        stats["detections"] += 1
        return True, "TOO_FREQUENT"
    
    return False, None

# --- ARP processing ---
def send_arp_request(sender, target_ip):
    log(f"{sender['name']}: ARP request for {target_ip}")
    stats["arp_requests"] += 1
    arp_history.append((time.time(), target_ip, None, "REQUEST"))
    
    if gateway["ip"] == target_ip:
        scheduled_replies.append((time.time() + GATEWAY_REPLY_DELAY, gateway, gateway['ip'], gateway['mac'], False))

def send_arp_reply(owner, target_ip, owner_mac, is_forged=False):
    reply_type = "FORGED" if is_forged else "legitimate"
    log(f"{owner['name']}: {reply_type} ARP reply {target_ip} is at {owner_mac}")
    
    if is_forged:
        stats["forged_replies"] += 1
    else:
        stats["legitimate_replies"] += 1
    
    arp_history.append((time.time(), target_ip, owner_mac, "REPLY" if not is_forged else "FORGED"))
    process_arp_reply(victim, target_ip, owner_mac, is_forged)

def send_forged_reply(attacker, claimed_ip, fake_mac):
    send_arp_reply(attacker, claimed_ip, fake_mac, is_forged=True)

def process_arp_reply(host, ip, mac, is_forged=False):
    prev = host['arp'].get(ip)
    
    # Static ARP check
    if static_arp_enabled and ip in host['arp']:
        log("Victim: static ARP enabled — ignoring update", "DEFENSE")
        return
    
    # Detection system
    suspicious, reason = detect_arp_anomaly(ip, mac, "REPLY")
    if suspicious:
        log(f"⚠️ ALERT: Suspicious ARP activity detected - {reason}", "ALERT")
        if auto_defend_enabled and is_forged:
            log("Auto-defense triggered: sending gratuitous ARP", "DEFENSE")
            scheduled_replies.append((time.time() + 0.1, gateway, gateway['ip'], gateway['mac'], False))
            stats["restorations"] += 1
    
    host['arp'][ip] = mac
    
    if prev is None:
        log(f"Victim: learned {ip} -> {mac}")
    elif prev != mac:
        log(f"Victim: UPDATED {ip}: {prev} -> {mac}", "WARNING")
        if prev == gateway['mac'] and mac != gateway['mac']:
            stats["cache_poisonings"] += 1
    
    update_flow_state()

# --- Visual / flow state ---
flow_state = "unknown"
alert_active = False

def update_flow_state():
    global flow_state, alert_active
    real = gateway['mac']
    mapped = victim['arp'].get(gateway['ip'])
    
    if mapped is None:
        flow_state = "unknown"
        alert_active = False
    elif mapped == real:
        flow_state = "ok"
        alert_active = False
    else:
        flow_state = "poisoned"
        alert_active = True

scheduled_replies = []

# --- Matplotlib setup ---
fig = plt.figure(figsize=(10, 7))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Main visualization
ax_main = fig.add_subplot(gs[0:2, :])
ax_main.set_xlim(0, 10)
ax_main.set_ylim(0, 6)
ax_main.axis('off')

# Statistics panel
ax_stats = fig.add_subplot(gs[2, 0])
ax_stats.axis('off')

# Log panel
ax_log = fig.add_subplot(gs[2, 1])
ax_log.axis('off')

plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

# positions
pos = {
    "victim": (2, 3),
    "gateway": (8, 4),
    "spoofer": (8, 1.5)
}

# draw nodes
node_patches = {}
for k, p in pos.items():
    circ = patches.Circle(p, 0.6, ec='black', lw=1.5, facecolor='#ddd')
    ax_main.add_patch(circ)
    node_patches[k] = circ
    ax_main.text(p[0], p[1]-1.0, k.capitalize(), ha='center', fontsize=10, weight='bold')

# flow line
flow_line, = ax_main.plot([pos['victim'][0], pos['gateway'][0]], 
                          [pos['victim'][1], pos['gateway'][1]],
                          lw=8, solid_capstyle='round', color='gray', alpha=0.6)

# Alert indicator
alert_circle = patches.Circle((5, 5), 0.3, ec='red', lw=3, facecolor='none', visible=False)
ax_main.add_patch(alert_circle)
alert_text = ax_main.text(5, 5, "!", ha='center', va='center', fontsize=20, 
                         color='red', weight='bold', visible=False)

# ARP cache box
arp_text = ax_main.text(0.02, 0.98, "", transform=ax_main.transAxes, va='top', fontsize=9,
                       bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

# Status indicators
status_text = ax_main.text(0.98, 0.98, "", transform=ax_main.transAxes, va='top', ha='right', 
                          fontsize=8, bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.3'))

# Stats display
stats_text = ax_stats.text(0.05, 0.95, "", transform=ax_stats.transAxes, va='top', fontsize=8,
                          bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

# Log display
log_text = ax_log.text(0.05, 0.95, "", transform=ax_log.transAxes, va='top', fontsize=7,
                      family='monospace', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

# Instructions
ax_main.text(0.5, 0.02, "Keys: r=restore | s=static ARP | d=detection | a=auto-defend | e=export log | l=start/stop logging | q=quit", 
            transform=ax_main.transAxes, ha='center', fontsize=9, 
            bbox=dict(facecolor='lightblue', alpha=0.7, boxstyle='round,pad=0.3'))

def update_frame(frame):
    global _last_arp_request, _last_spoof, alert_active
    tnow = time.time()
    
    # Victim ARP requests
    if tnow - _last_arp_request >= ARP_REQUEST_INTERVAL:
        _last_arp_request = tnow
        send_arp_request(victim, gateway['ip'])
    
    # Spoofer attacks
    if tnow - _last_spoof >= SPOOFER_INTERVAL:
        _last_spoof = tnow
        if random.random() < 0.9:
            send_forged_reply(spoofer, gateway['ip'], spoofer['mac'])
    
    # Fire scheduled replies
    if scheduled_replies:
        for sched in scheduled_replies[:]:
            fire_time, owner, ip, mac, is_forged = sched
            if tnow >= fire_time:
                send_arp_reply(owner, ip, mac, is_forged)
                scheduled_replies.remove(sched)
    
    # Update visuals
    node_patches['victim'].set_facecolor('#bfefff' if not static_arp_enabled else '#c7f5c7')
    node_patches['gateway'].set_facecolor('#d1ffd1')
    node_patches['spoofer'].set_facecolor('#ffd1d1')
    
    # Alert animation
    if alert_active:
        alert_circle.set_visible(True)
        alert_text.set_visible(True)
        # Pulse effect
        scale = 1 + 0.3 * abs(time.time() % 1 - 0.5)
        alert_circle.set_radius(0.3 * scale)
    else:
        alert_circle.set_visible(False)
        alert_text.set_visible(False)
    
    # Flow line color
    if flow_state == "unknown":
        flow_line.set_color('gray')
        flow_line.set_alpha(0.4)
    elif flow_state == "ok":
        flow_line.set_color('green')
        flow_line.set_alpha(0.9)
    else:
        flow_line.set_color('red')
        flow_line.set_alpha(0.9)
    
    # Update ARP cache display
    s = "📋 Victim ARP Cache:\n"
    for ip, mac in victim['arp'].items():
        indicator = "✓" if mac == gateway['mac'] else "✗"
        s += f"{indicator} {ip} → {mac}\n"
    if not victim['arp']:
        s += "(empty)\n"
    arp_text.set_text(s)
    
    # Update status
    status = "🔒 Status:\n"
    status += f"Static ARP: {'ON' if static_arp_enabled else 'OFF'}\n"
    status += f"Detection: {'ON' if detection_enabled else 'OFF'}\n"
    status += f"Auto-defend: {'ON' if auto_defend_enabled else 'OFF'}\n"
    status += f"Logging: {'ON' if log_file else 'OFF'}\n"
    status_text.set_text(status)
    
    # Update statistics
    stats_display = "📊 Statistics:\n"
    stats_display += f"ARP Requests: {stats['arp_requests']}\n"
    stats_display += f"Legitimate Replies: {stats['legitimate_replies']}\n"
    stats_display += f"Forged Replies: {stats['forged_replies']}\n"
    stats_display += f"Cache Poisonings: {stats['cache_poisonings']}\n"
    stats_display += f"Detections: {stats['detections']}\n"
    stats_display += f"Restorations: {stats['restorations']}\n"
    if stats['forged_replies'] > 0:
        success_rate = (stats['cache_poisonings'] / stats['forged_replies']) * 100
        stats_display += f"Attack Success: {success_rate:.1f}%\n"
    stats_text.set_text(stats_display)
    
    # Update log
    log_text.set_text("\n".join(LOG_LINES[-8:]))
    
    return []

def on_key(event):
    global static_arp_enabled, detection_enabled, auto_defend_enabled
    
    if event.key == 'r':
        log("🛡️ Manual restoration: sending correct gratuitous ARP", "ACTION")
        send_arp_reply(gateway, gateway['ip'], gateway['mac'])
        stats["restorations"] += 1
    
    elif event.key == 's':
        static_arp_enabled = not static_arp_enabled
        log(f"🔒 Static ARP: {static_arp_enabled}", "ACTION")
        if static_arp_enabled:
            victim['arp'][gateway['ip']] = gateway['mac']
            update_flow_state()
    
    elif event.key == 'd':
        detection_enabled = not detection_enabled
        log(f"🔍 Detection system: {detection_enabled}", "ACTION")
    
    elif event.key == 'a':
        auto_defend_enabled = not auto_defend_enabled
        log(f"⚔️ Auto-defend mode: {auto_defend_enabled}", "ACTION")
    
    elif event.key == 'e':
        filename = f"arp_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write("=== ARP Spoofing Simulation Statistics ===\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("--- Statistics ---\n")
            for key, value in stats.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            f.write("\n--- Recent Log ---\n")
            for line in LOG_LINES:
                f.write(line + "\n")
            f.write("\n--- ARP History ---\n")
            for ts, ip, mac, etype in arp_history[-50:]:
                timestr = datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                f.write(f"{timestr} | {ip} | {mac} | {etype}\n")
        log(f"📄 Exported statistics to {filename}", "SYSTEM")
    
    elif event.key == 'l':
        if log_file:
            stop_logging()
        else:
            start_logging()
    
    elif event.key == 'q':
        log("Shutting down simulation", "SYSTEM")
        if log_file:
            stop_logging()
        plt.close(fig)

fig.canvas.mpl_connect('key_press_event', on_key)

# Start
ani = animation.FuncAnimation(fig, update_frame, interval=FRAME_INTERVAL_MS)
log("Extended simulation ready! Additional features: detection, auto-defend, logging", "SYSTEM")
log("Press 'd' for detection, 'a' for auto-defend, 'l' to start logging", "SYSTEM")
plt.suptitle("ARP Spoofing — Extended Simulation (Detection + Logging)", fontsize=12, weight='bold')
plt.show()
