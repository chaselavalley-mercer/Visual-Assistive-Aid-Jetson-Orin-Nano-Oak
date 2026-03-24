# Laptop to Jetson Workflow

This guide explains exactly how to:
1. set up the project on a laptop,
2. test the OAK camera on the laptop,
3. SSH from the laptop into the Jetson Orin Nano,
4. set up the same repo on the Jetson,
5. run the same tests on the Jetson.

Use this as the step-by-step checklist for tomorrow.

---

## 1. What you need before starting

Have all of this ready:
- your laptop
- the OAK camera
- a USB cable for the OAK camera
- the Jetson Orin Nano
- power for the Jetson
- the same Wi-Fi network for both laptop and Jetson, or Ethernet if available
- the GitHub repo URL
- VS Code installed on the laptop
- Python installed on the laptop

Recommended repo name:
`Visual-Assistive-Aid-Jetson-Orin-Nano-Oak`

---

## 2. Clone the repo on the laptop

Open **PowerShell** or the **VS Code terminal** on the laptop.

Go to the folder where you want the project:

```powershell
cd C:\Projects
```

Clone the repo:

```powershell
git clone https://github.com/YOUR_USERNAME/Visual-Assistive-Aid-Jetson-Orin-Nano-Oak.git
```

Go into the repo:

```powershell
cd .\Visual-Assistive-Aid-Jetson-Orin-Nano-Oak
```

Open it in VS Code:

```powershell
code .
```

---

## 3. Create the Python virtual environment on the laptop

In the terminal inside the repo folder, run:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the script, run this first:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should now see `(.venv)` in the terminal.

---

## 4. Install the requirements on the laptop

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install all project packages:

```powershell
pip install -r requirements.txt
```

If `requirements.txt` is missing something, install the basics manually:

```powershell
pip install depthai opencv-python numpy
```

---

## 5. Make sure VS Code uses the correct interpreter

In VS Code:
1. Press `Ctrl+Shift+P`
2. Search for `Python: Select Interpreter`
3. Choose the interpreter inside this repo’s `.venv`

It should look something like:

```text
...\Visual-Assistive-Aid-Jetson-Orin-Nano-Oak\.venv\Scripts\python.exe
```

This step matters. If VS Code uses the wrong interpreter, it may say `depthai` or `cv2` is missing even if you installed them.

---

## 6. Test the imports on the laptop

Run this in the terminal:

```powershell
python -c "import depthai, cv2, numpy; print('imports ok')"
```

If that prints `imports ok`, your Python environment is ready.

---

## 7. Connect the OAK camera to the laptop

Plug the OAK camera into the laptop with a good USB cable.

Then run:

```powershell
python scripts/check_oak.py
```

If that works, run:

```powershell
python scripts/test_rgb_preview.py
```

Then run:

```powershell
python scripts/test_depth_preview.py
```

### Goal for this stage
You want to prove:
- the laptop sees the camera
- Python can talk to the camera
- RGB preview works
- depth preview works

If these do not work on the laptop, do **not** move on to the Jetson yet.

---

## 8. Prepare the Jetson for SSH

The Jetson must be:
- powered on
- connected to the same network as the laptop
- fully booted

If you have a monitor connected to the Jetson, log in locally first.

### Find the Jetson IP address
On the Jetson terminal, run:

```bash
hostname -I
```

This should print an IP address like:

```bash
192.168.1.45
```

Write that down.

### Make sure SSH is installed and running on the Jetson
On the Jetson, run:

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh
```

You want to see that the SSH service is active.

---

## 9. SSH into the Jetson from the laptop

On the laptop terminal, run:

```powershell
ssh YOUR_JETSON_USERNAME@JETSON_IP_ADDRESS
```

Example:

```powershell
ssh chase@192.168.1.45
```

The first time, it may ask if you trust the host. Type:

```text
yes
```

Then enter the Jetson password.

If it works, you are now controlling the Jetson from the laptop terminal.

---

## 10. Clone the repo on the Jetson

Once inside the SSH session, go to the folder where you want the project:

```bash
mkdir -p ~/Projects
cd ~/Projects
```

Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/Visual-Assistive-Aid-Jetson-Orin-Nano-Oak.git
```

Go into the repo:

```bash
cd Visual-Assistive-Aid-Jetson-Orin-Nano-Oak
```

---

## 11. Set up the Jetson Python environment

Run the Jetson setup script:

```bash
chmod +x scripts/setup_jetson.sh
./scripts/setup_jetson.sh
```

Then activate the virtual environment:

```bash
source .venv/bin/activate
```

You should now see `(.venv)` in the terminal.

### Confirm the packages installed
Run:

```bash
python -c "import depthai, cv2, numpy; print('imports ok on jetson')"
```

---

## 12. Connect the OAK camera to the Jetson

Now unplug the OAK from the laptop and connect it to the Jetson.

Use a good USB cable.

Then on the Jetson, run:

```bash
python scripts/check_oak.py
```

If that works, run:

```bash
python scripts/test_rgb_preview.py
```

Then run:

```bash
python scripts/test_depth_preview.py
```

---

## 13. Important note about preview windows over SSH

If you run the preview scripts through SSH, OpenCV windows may fail to open or may not display correctly.

That does **not** always mean the script is broken.

### Lowest-risk approach
If `check_oak.py` works over SSH but preview windows do not open:
- keep using SSH for setup and file management
- run the preview scripts directly on the Jetson with a monitor/desktop attached

So the order is:
- laptop preview tests on laptop
- Jetson device detection by SSH is okay
- Jetson preview tests are safest on the Jetson’s own display session

---

## 14. What “success” looks like tomorrow

By the end of tomorrow, you want all of these done:

### Laptop
- repo cloned
- `.venv` created
- requirements installed
- OAK detected
- RGB preview works
- depth preview works

### Jetson
- SSH works
- repo cloned
- Jetson setup script runs
- `.venv` created
- requirements installed
- OAK detected on Jetson
- RGB/depth tests attempted on Jetson

If you reach that point, tomorrow is a success.

---

## 15. Fast troubleshooting checklist

### Problem: `depthai` or `cv2` not found
Fix:
- activate `.venv`
- run `pip install -r requirements.txt`
- make sure VS Code selected the correct interpreter

### Problem: OAK not detected
Fix:
- check USB cable
- reconnect device
- restart script
- try another USB port

### Problem: SSH fails
Fix:
- confirm Jetson IP with `hostname -I`
- confirm SSH service is running
- confirm laptop and Jetson are on the same network

### Problem: preview window does not open on Jetson over SSH
Fix:
- run preview locally on the Jetson with a monitor attached
- still use SSH for setup and running non-GUI checks

---

## 16. Commands summary

### Laptop setup
```powershell
cd C:\Projects
git clone https://github.com/YOUR_USERNAME/Visual-Assistive-Aid-Jetson-Orin-Nano-Oak.git
cd .\Visual-Assistive-Aid-Jetson-Orin-Nano-Oak
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import depthai, cv2, numpy; print('imports ok')"
python scripts/check_oak.py
python scripts/test_rgb_preview.py
python scripts/test_depth_preview.py
```

### Jetson setup
```bash
hostname -I
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable ssh
sudo systemctl start ssh
ssh YOUR_JETSON_USERNAME@JETSON_IP_ADDRESS
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/YOUR_USERNAME/Visual-Assistive-Aid-Jetson-Orin-Nano-Oak.git
cd Visual-Assistive-Aid-Jetson-Orin-Nano-Oak
chmod +x scripts/setup_jetson.sh
./scripts/setup_jetson.sh
source .venv/bin/activate
python -c "import depthai, cv2, numpy; print('imports ok on jetson')"
python scripts/check_oak.py
python scripts/test_rgb_preview.py
python scripts/test_depth_preview.py
```

---

## 17. Final recommendation

Do not try to do everything at once.

Use this order tomorrow:
1. laptop environment
2. laptop OAK test
3. Jetson SSH
4. Jetson repo setup
5. Jetson OAK test

That is the fastest low-risk path.
