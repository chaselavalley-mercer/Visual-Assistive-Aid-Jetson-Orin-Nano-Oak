# Visual Assistive Aid Jetson Orin Nano Oak

Python-first starter repo for bringing up a Luxonis OAK-D Lite with a Jetson Orin Nano using GitHub and VS Code.

## Locked-in stack
- **Language:** Python
- **Version control:** Git + GitHub
- **Main IDE:** VS Code
- **Target device:** Jetson Orin Nano
- **Camera:** Luxonis OAK-D Lite

## Goal for tomorrow
1. Create the GitHub repo.
2. Clone it on your main computer.
3. Push this starter structure.
4. Clone it on the Jetson.
5. Run `check_oak.py`.
6. Run `test_rgb_preview.py`.
7. Run `test_depth_preview.py`.

## Repo layout
- `requirements.txt` - Python dependencies
- `.gitignore` - common Python / VS Code ignores
- `scripts/setup_local.sh` - local Linux/macOS-style Python setup
- `scripts/setup_jetson.sh` - Jetson setup script
- `scripts/check_oak.py` - minimal OAK detection test
- `scripts/test_rgb_preview.py` - RGB preview test
- `scripts/test_depth_preview.py` - depth preview test
- `docs/jetson_setup.md` - Jetson setup checklist
- `docs/github_vscode_workflow.md` - branch / merge workflow
- `docs/tomorrow_bringup_checklist.md` - fastest path to camera validation
- `CONTRIBUTING.md` - team branching / push / pull / merge rules

## Fast start
### 1. Create the GitHub repo
Use the exact repo name:
`Visual-Assistive-Aid-Jetson-Orin-Nano-Oak`

### 2. Clone locally
```bash
git clone <your-repo-url>
cd Visual-Assistive-Aid-Jetson-Orin-Nano-Oak
```

### 3. Create and activate venv (windows)
.\scripts\setup_windows.ps1
.\.venv\Scripts\Activate.ps1

### 3. Create and activate venv (Mac)
./scripts/setup_local.sh
source .venv/bin/activate

### 3. Create and activate venv (Jetson)
chmod +x scripts/setup_jetson.sh
./scripts/setup_jetson.sh
source .venv/bin/activate

### 4. First test
```bash
python scripts/check_oak.py
```

### 5. RGB test
```bash
python scripts/test_rgb_preview.py
```

### 6. Depth test
```bash
python scripts/test_depth_preview.py
```

## Suggested first branches
- `main` -> stable only
- `dev/chase-jetson-setup`
- `dev/<teammate-name>-oak-tests`
- `feature/obstacle-zones`
- `feature/audio-feedback`

## First commit suggestions
- `init: add starter repo structure`
- `test: verify oak detected on laptop`
- `test: verify oak detected on jetson`
- `feat: add obstacle zone prototype`

## Notes
- Python is the right choice for the two-week deadline.
- Keep `main` stable; do new work in branches.
- Do not wait to test on Jetson. Move there early.
