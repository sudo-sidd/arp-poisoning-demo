#!/usr/bin/env python3
"""
run_demo.py - Interactive demo launcher for ARP spoofing simulation
Easy entry point with guided options for presentations and learning
"""

import os
import sys
import subprocess

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display welcome banner"""
    banner = r"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         ARP Spoofing Simulation - Demo Launcher          ║
    ║                                                           ║
    ║          Safe, Educational, No Real Network Traffic       ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_menu():
    """Display main menu"""
    print("\n📚 Choose a demo mode:\n")
    print("  1. Basic Simulation (Quick Start)")
    print("     └─ Simple visualization, perfect for first-time users")
    print()
    print("  2. Extended Simulation (Advanced Features)")
    print("     └─ Detection, auto-defend, logging, statistics")
    print()
    print("  3. Guided Tutorial (Step-by-Step)")
    print("     └─ Interactive walkthrough with instructions")
    print()
    print("  4. View Documentation")
    print("     └─ Open README, DEMO_GUIDE, or THEORY docs")
    print()
    print("  5. Check Installation")
    print("     └─ Verify Python and dependencies")
    print()
    print("  0. Exit")
    print()

def run_basic_sim():
    """Launch basic simulation"""
    clear_screen()
    print("🚀 Starting Basic ARP Simulation...\n")
    print("Instructions:")
    print("  • Press 'r' to send gratuitous ARP (restore correct mapping)")
    print("  • Press 's' to toggle static ARP (defense)")
    print("  • Press 'q' to quit")
    print("\nWatch for:")
    print("  • Gray line = No ARP mapping")
    print("  • Green line = Correct mapping (safe)")
    print("  • Red line = Poisoned mapping (attack active)")
    print("\n" + "="*60)
    input("\nPress Enter to launch simulation...")
    
    try:
        subprocess.run([sys.executable, "arp_sim.py"])
    except FileNotFoundError:
        print("\n❌ Error: arp_sim.py not found in current directory")
        print("Make sure you're running from the CN-demo folder")
    except Exception as e:
        print(f"\n❌ Error running simulation: {e}")

def run_extended_sim():
    """Launch extended simulation"""
    clear_screen()
    print("🚀 Starting Extended ARP Simulation...\n")
    print("Additional Features:")
    print("  • Press 'd' to toggle attack detection")
    print("  • Press 'a' to toggle auto-defend mode")
    print("  • Press 'l' to start/stop logging to file")
    print("  • Press 'e' to export statistics and logs")
    print("\nStatistics Panel:")
    print("  • Tracks all ARP events")
    print("  • Shows attack success rate")
    print("  • Displays detection count")
    print("\n" + "="*60)
    input("\nPress Enter to launch extended simulation...")
    
    try:
        subprocess.run([sys.executable, "arp_sim_extended.py"])
    except FileNotFoundError:
        print("\n❌ Error: arp_sim_extended.py not found")
        print("Make sure you're running from the CN-demo folder")
    except Exception as e:
        print(f"\n❌ Error running simulation: {e}")

def run_guided_tutorial():
    """Interactive guided tutorial"""
    clear_screen()
    print("📖 Guided Tutorial - ARP Spoofing Simulation\n")
    print("="*60)
    
    print("\n🎯 What You'll Learn:")
    print("  1. How ARP protocol works")
    print("  2. How ARP spoofing attacks work")
    print("  3. Defense mechanisms and their trade-offs")
    
    input("\n▶ Press Enter to continue...")
    
    clear_screen()
    print("📡 Part 1: Understanding ARP\n")
    print("="*60)
    print("\nARP (Address Resolution Protocol) maps IP addresses to MAC addresses.")
    print("\nExample:")
    print("  Victim (192.168.1.10) wants to talk to Gateway (192.168.1.1)")
    print("  Victim asks: 'Who has 192.168.1.1?'")
    print("  Gateway replies: '192.168.1.1 is at GG:GG:GG:GG:GG:01'")
    print("  Victim stores this in ARP cache")
    
    input("\n▶ Press Enter to continue...")
    
    clear_screen()
    print("⚠️ Part 2: The Attack\n")
    print("="*60)
    print("\nProblem: ARP has NO authentication!")
    print("\nAttacker can send fake ARP reply:")
    print("  Spoofer says: '192.168.1.1 is at SS:SS:SS:SS:SS:80' (LIE!)")
    print("  Victim believes it and updates cache")
    print("  Victim now sends Gateway traffic to Spoofer")
    print("\nThis is a Man-in-the-Middle (MITM) attack!")
    
    input("\n▶ Press Enter to see live demo...")
    
    # Run simulation in tutorial mode
    print("\n🎬 Starting simulation...")
    print("\nWatch for these phases:")
    print("  Phase 1 (0-3s): Gray line - No ARP mapping yet")
    print("  Phase 2 (3-6s): Green line - Legitimate ARP exchange")
    print("  Phase 3 (6+s): Red line - Attack! Cache is poisoned")
    print("\nTry pressing 'r' to restore (but watch it get re-poisoned)")
    print("Then press 's' to enable static ARP (immune to attacks)")
    
    input("\n▶ Press Enter to launch...")
    run_basic_sim()

def view_docs():
    """Open documentation"""
    clear_screen()
    print("📚 Documentation\n")
    print("="*60)
    print("\nAvailable documents:")
    print("  1. README.md - Quick start and overview")
    print("  2. DEMO_GUIDE.md - Step-by-step walkthroughs")
    print("  3. THEORY.md - Deep dive into ARP protocol")
    print("  4. SETUP.md - Installation instructions")
    print("  0. Back to main menu")
    
    choice = input("\n▶ Select document (0-4): ").strip()
    
    doc_files = {
        '1': 'README.md',
        '2': 'DEMO_GUIDE.md',
        '3': 'THEORY.md',
        '4': 'SETUP.md'
    }
    
    if choice in doc_files:
        doc = doc_files[choice]
        if os.path.exists(doc):
            # Try to open with default viewer
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(doc)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', doc])
                else:  # Linux
                    subprocess.run(['xdg-open', doc])
                print(f"\n✓ Opened {doc} in default viewer")
            except:
                # Fallback: print to console
                print(f"\n📄 Contents of {doc}:\n")
                with open(doc, 'r', encoding='utf-8') as f:
                    print(f.read())
        else:
            print(f"\n❌ File not found: {doc}")
    
    input("\n▶ Press Enter to continue...")

def check_installation():
    """Verify installation and dependencies"""
    clear_screen()
    print("🔍 Checking Installation...\n")
    print("="*60)
    
    # Check Python version
    print("\n1. Python Version:")
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 7:
        print(f"   ✓ Python {py_version.major}.{py_version.minor}.{py_version.micro} (OK)")
    else:
        print(f"   ✗ Python {py_version.major}.{py_version.minor}.{py_version.micro} (Need 3.7+)")
    
    # Check matplotlib
    print("\n2. Matplotlib:")
    try:
        import matplotlib
        print(f"   ✓ matplotlib {matplotlib.__version__} (OK)")
    except ImportError:
        print("   ✗ matplotlib not installed")
        print("   Run: pip install matplotlib")
    
    # Check files
    print("\n3. Required Files:")
    required_files = ['arp_sim.py', 'arp_sim_extended.py', 'README.md', 'requirements.txt']
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} (missing)")
    
    # System info
    print("\n4. System Information:")
    print(f"   OS: {os.name}")
    print(f"   Platform: {sys.platform}")
    print(f"   Current Directory: {os.getcwd()}")
    
    print("\n" + "="*60)
    
    # Check if ready to run
    try:
        import matplotlib
        if os.path.exists('arp_sim.py'):
            print("\n✅ All checks passed! Ready to run simulations.")
        else:
            print("\n⚠️ Some files are missing. Check project structure.")
    except ImportError:
        print("\n⚠️ Missing dependencies. Run: pip install -r requirements.txt")
    
    input("\n▶ Press Enter to continue...")

def main():
    """Main menu loop"""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        choice = input("▶ Select an option (0-5): ").strip()
        
        if choice == '1':
            run_basic_sim()
        elif choice == '2':
            run_extended_sim()
        elif choice == '3':
            run_guided_tutorial()
        elif choice == '4':
            view_docs()
        elif choice == '5':
            check_installation()
        elif choice == '0':
            clear_screen()
            print("\n👋 Thanks for using ARP Spoofing Simulation!")
            print("Stay curious. Stay ethical. Stay secure.\n")
            sys.exit(0)
        else:
            input("\n❌ Invalid choice. Press Enter to try again...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\n👋 Interrupted. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue if it persists.")
        sys.exit(1)
