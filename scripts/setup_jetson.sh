#!/usr/bin/env bash
set -euo pipefail

echo "Updating apt packages..."
sudo apt update
sudo apt upgrade -y

echo "Installing Jetson/DepthAI dependencies..."
sudo apt install -y python3-venv python3-pip git usbutils

# Luxonis dependency installer
wget -qO- https://docs.luxonis.com/install_dependencies.sh | bash

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

if ! grep -q 'OPENBLAS_CORETYPE=ARMV8' ~/.bashrc; then
  echo 'export OPENBLAS_CORETYPE=ARMV8' >> ~/.bashrc
fi

echo "Jetson setup complete. Reopen terminal or run: source ~/.bashrc"
echo "Then activate your venv with: source .venv/bin/activate"
