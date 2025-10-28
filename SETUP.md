# Quick Setup Guide

## Windows PowerShell Setup

```powershell
# Navigate to project directory
cd d:\Projects\CN-demo

# Install Python dependencies
pip install -r requirements.txt

# Run the simulation
python arp_sim.py
```

## Linux / macOS Setup

```bash
# Navigate to project directory
cd ~/Projects/CN-demo

# Install Python dependencies
pip3 install -r requirements.txt

# Run the simulation
python3 arp_sim.py
```

## Verifying Installation

```powershell
# Check Python version (needs 3.7+)
python --version

# Check if matplotlib is installed
python -c "import matplotlib; print(matplotlib.__version__)"
```

## Troubleshooting

### Issue: pip not found
**Solution**: Install Python from https://python.org or use `py -m pip install -r requirements.txt`

### Issue: Permission denied
**Solution Windows**: Run as Administrator
**Solution Linux/Mac**: Use `sudo pip3 install -r requirements.txt`

### Issue: Matplotlib won't display
**Solution**: Try different backend by adding at top of arp_sim.py:
```python
import matplotlib
matplotlib.use('TkAgg')
```

## What Gets Installed

- **matplotlib**: For visualization and animation (required)
- No other dependencies needed for basic simulation

## Next Steps

1. Read [README.md](./README.md) for full documentation
2. Follow [DEMO_GUIDE.md](./DEMO_GUIDE.md) for walkthroughs
3. Study [THEORY.md](./THEORY.md) for deep understanding
