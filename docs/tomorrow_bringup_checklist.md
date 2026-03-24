# Tomorrow Bring-Up Checklist

## Success criteria
By the end of tomorrow, you want proof of all three:
- Jetson sees OAK-D Lite
- RGB preview opens
- Depth preview opens

## On your main computer
1. Create GitHub repo: `Visual-Assistive-Aid-Jetson-Orin-Nano-Oak`
2. Clone repo
3. Open in VS Code
4. Push starter files

## On the Jetson
1. Clone repo
2. Run setup script
```bash
chmod +x scripts/setup_jetson.sh
./scripts/setup_jetson.sh
```
3. Activate venv
```bash
source .venv/bin/activate
```
4. Plug in OAK-D Lite
5. Check USB detection
```bash
lsusb | grep 03e7 || true
```
6. Run device check
```bash
python scripts/check_oak.py
```
7. Run RGB test
```bash
python scripts/test_rgb_preview.py
```
8. Run depth test
```bash
python scripts/test_depth_preview.py
```

## If camera is not detected
- try a different USB 3 cable
- try a different USB port
- reboot Jetson
- rerun the venv and dependency steps
- re-run `python scripts/check_oak.py`

## If previews do not open
- confirm monitor / desktop session exists on Jetson
- if headless, use X forwarding or temporarily test from a local Jetson desktop session
- confirm OpenCV installed correctly inside `.venv`

## What to commit tomorrow
- updated README if needed
- any Jetson-specific fixes
- proof that the first three tests run
