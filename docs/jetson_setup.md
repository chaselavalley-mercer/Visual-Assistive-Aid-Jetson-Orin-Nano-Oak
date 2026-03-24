# Jetson Orin Nano + OAK-D Lite Setup

## 1. Flash / update Jetson first
- If your Orin Nano is still on older firmware or JetPack 5.x, update firmware before moving to JetPack 6.2.
- If already on JetPack 6.x, use the correct JetPack 6.2 SD image or package flow.

## 2. Install JetPack components
```bash
sudo apt update
sudo apt install nvidia-jetpack
```

## 3. Clone your repo
```bash
git clone <your-repo-url>
cd oak-jetson-starter
```

## 4. Run the Jetson setup script
```bash
chmod +x scripts/setup_jetson.sh
./scripts/setup_jetson.sh
```

## 5. Activate the venv
```bash
source .venv/bin/activate
```

## 6. Plug in OAK-D Lite via USB 3
Use a reliable USB 3 cable.

## 7. Check Linux sees the device
```bash
lsusb | grep 03e7
```

## 8. Run camera tests
```bash
python scripts/check_oak.py
python scripts/test_rgb_preview.py
python scripts/test_depth_preview.py
```

## 9. Preferred dev workflow
Use VS Code Remote-SSH into the Jetson, edit there, run there, commit back to GitHub.
