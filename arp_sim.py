# arp_sim.py
# Safe ARP spoofing simulation and visualization
# Requires: Python 3.x and matplotlib
# Run: python arp_sim.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import random
import time

# --- Simulation Parameters ---
ARP_REQUEST_INTERVAL = 3.0    # seconds between Victim ARP requests
GATEWAY_REPLY_DELAY = 0.4     # delay before Gateway replies
SPOOFER_INTERVAL = 2.0        # how often Spoofer injects forged replies
FRAME_INTERVAL_MS = 200       # animation frame interval (ms)

# --- Node definitions ---
victim = {
    "name": "Victim",
    "ip": "192.168.1.10",
    "mac": "AA:AA:AA:AA:AA:10",
    "arp": {}   # arp cache (ip -> mac)
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

# --- Internal timing state ---
_last_arp_request = time.time()
_last_spoof = time.time()
static_arp_enabled = False

# --- Logging helper ---
LOG_LINES = []
def log(msg):
    t = time.strftime("%H:%M:%S")
    LOG_LINES.append(f"[{t}] {msg}")
    if len(LOG_LINES) > 8:
        LOG_LINES.pop(0)
    print(LOG_LINES[-1])

# --- ARP processing (simulated) ---
def send_arp_request(sender, target_ip):
    log(f"{sender['name']}: ARP request for {target_ip}")
    # Gateway replies after a small delay
    if gateway["ip"] == target_ip:
        # schedule reply (we just sleep a tiny bit to simulate delay)
        scheduled_replies.append( (time.time() + GATEWAY_REPLY_DELAY, gateway, gateway['ip'], gateway['mac']) )

def send_arp_reply(owner, target_ip, owner_mac):
    log(f"{owner['name']}: ARP reply {owner['ip']} is at {owner_mac}")
    process_arp_reply(victim, owner['ip'], owner_mac)

def send_forged_reply(attacker, claimed_ip, fake_mac):
    log(f"{attacker['name']}: FORGED ARP reply claiming {claimed_ip} is at {fake_mac}")
    process_arp_reply(victim, claimed_ip, fake_mac)

def process_arp_reply(host, ip, mac):
    prev = host['arp'].get(ip)
    # If static ARP enabled, ignore updates to that mapping
    if static_arp_enabled and ip in host['arp']:
        log("Victim: static ARP enabled — ignoring update")
        return
    host['arp'][ip] = mac
    if prev is None:
        log(f"Victim: learned {ip} -> {mac}")
    elif prev != mac:
        log(f"Victim: UPDATED {ip}: {prev} -> {mac}")
    update_flow_state()

# --- Visual / flow state ---
flow_state = "unknown"  # "unknown", "ok", "poisoned"
def update_flow_state():
    real = gateway['mac']
    mapped = victim['arp'].get(gateway['ip'])
    global flow_state
    if mapped is None:
        flow_state = "unknown"
    elif mapped == real:
        flow_state = "ok"
    else:
        flow_state = "poisoned"

# scheduled replies list: tuples (time_to_fire, owner, ip, mac)
scheduled_replies = []

# --- Matplotlib setup ---
fig, ax = plt.subplots(figsize=(6,4))
plt.subplots_adjust(left=0.02, right=0.98, top=0.92, bottom=0.06)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# positions
pos = {
    "victim": (2, 3),
    "gateway": (8, 4),
    "spoofer": (8, 1.5)
}

# draw nodes (circles with labels)
node_patches = {}
for k,p in pos.items():
    circ = patches.Circle(p, 0.6, ec='black', lw=1.5, facecolor='#ddd')
    ax.add_patch(circ)
    node_patches[k] = circ
    ax.text(p[0], p[1]-1.0, k.capitalize(), ha='center', fontsize=10)

# arrow for flow (line)
flow_line, = ax.plot([pos['victim'][0], pos['gateway'][0]], [pos['victim'][1], pos['gateway'][1]],
                     lw=6, solid_capstyle='round', color='gray', alpha=0.6)

# ARP cache box
arp_text = ax.text(0.5, 0.95, "", transform=ax.transAxes, va='top', fontsize=9,
                   bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

# Log text
log_text = ax.text(0.5, 0.45, "", transform=ax.transAxes, va='top', fontsize=8,
                   bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

# instructions
ax.text(0.02, 0.02, "Keys: r=gratuitous ARP, s=toggle static ARP, q=quit", transform=ax.transAxes, fontsize=8)

# update visuals each frame
def update_frame(frame):
    global _last_arp_request, _last_spoof
    tnow = time.time()
    # Victim ARP requests periodically
    if tnow - _last_arp_request >= ARP_REQUEST_INTERVAL:
        _last_arp_request = tnow
        send_arp_request(victim, gateway['ip'])
    # Spoofer injects forged replies periodically
    if tnow - _last_spoof >= SPOOFER_INTERVAL:
        _last_spoof = tnow
        # chance to send, to make it interesting
        if random.random() < 0.9:
            send_forged_reply(spoofer, gateway['ip'], spoofer['mac'])
    # fire any scheduled replies
    if scheduled_replies:
        # copy to avoid mutation during iteration
        for sched in scheduled_replies[:]:
            fire_time, owner, ip, mac = sched
            if tnow >= fire_time:
                send_arp_reply(owner, ip, mac)
                scheduled_replies.remove(sched)
    # update node visuals
    node_patches['victim'].set_facecolor('#bfefff' if not static_arp_enabled else '#c7f5c7')
    node_patches['gateway'].set_facecolor('#d1ffd1')
    node_patches['spoofer'].set_facecolor('#ffd1d1')
    # update flow line color
    if flow_state == "unknown":
        flow_line.set_color('gray')
        flow_line.set_alpha(0.4)
    elif flow_state == "ok":
        flow_line.set_color('green')
        flow_line.set_alpha(0.9)
    else:
        flow_line.set_color('red')
        flow_line.set_alpha(0.9)
    # update ARP text box
    s = f"Victim ARP Cache (IP -> MAC):\n"
    for ip,mac in victim['arp'].items():
        s += f"{ip} -> {mac}\n"
    if not victim['arp']:
        s += "(empty)\n"
    arp_text.set_text(s)
    # update log text
    log_text.set_text("\n".join(LOG_LINES[-6:]))
    return []

# key event handlers
def on_key(event):
    global static_arp_enabled
    if event.key == 'r':
        # gratuitous/correct ARP from gateway to repair mapping
        log("Player action: send correct gratuitous ARP from Gateway")
        send_arp_reply(gateway, gateway['ip'], gateway['mac'])
    elif event.key == 's':
        static_arp_enabled = not static_arp_enabled
        log(f"Player action: toggle static ARP -> {static_arp_enabled}")
        if static_arp_enabled:
            # set static mapping to correct gateway mac
            victim['arp'][gateway['ip']] = gateway['mac']
            update_flow_state()
    elif event.key == 'q':
        log("Quitting simulation.")
        plt.close(fig)

fig.canvas.mpl_connect('key_press_event', on_key)

# start animation
ani = animation.FuncAnimation(fig, update_frame, interval=FRAME_INTERVAL_MS)
log("Simulation ready. Press 'r' to restore, 's' to toggle static ARP.")
plt.title("ARP Spoofing — Simulation (safe, no real network traffic)")
plt.show()
