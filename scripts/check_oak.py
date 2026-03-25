"""Minimal OAK detection test.

Run:
    python scripts/check_oak.py
"""

from __future__ import annotations

import sys

import depthai as dai


def main() -> int:
    devices = dai.Device.getAllAvailableDevices()
    if not devices:
        print("No OAK devices found.")
        print("Check USB cable, power, and whether the camera is detected by the OS.")
        return 1

    print(f"Found {len(devices)} device(s):")
    for idx, device_info in enumerate(devices, start=1):
        mxid = getattr(device_info, "mxid", None) or getattr(device_info, "getMxId", lambda: None)()
        print(f"  [{idx}] MX ID: {mxid}")
        print(f"      Name: {device_info.name}")

    with dai.Device(dai.DeviceInfo(), dai.UsbSpeed.HIGH) as device:
        print("\nConnected successfully.")
        print(f"Connected cameras: {device.getConnectedCameraFeatures()}")
        print(f"USB speed: {device.getUsbSpeed()}")
        print(f"Device name: {device.getDeviceName()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
