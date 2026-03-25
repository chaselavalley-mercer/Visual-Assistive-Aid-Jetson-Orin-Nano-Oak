
import depthai as dai
from typing import List


def main():
  print('Searching for all available devices...\n')
  infos: List[dai.DeviceInfo] = dai.Device.getAllAvailableDevices()

  if len(infos) == 0:
      print("Couldn't find any available devices.")
      exit(-1)


  for info in infos:
      # Converts enum eg. 'XLinkDeviceState.X_LINK_UNBOOTED' to 'UNBOOTED'
      state = str(info.state).split('X_LINK_')[1]

      print(f"Found device '{info.name}', DeviceID: '{info.deviceId}', State: '{state}'")


  # Connect to a specific device. We will just take the first one
  print(f"\nBooting the first available camera ({infos[0].name})...")
  with dai.Device(infos[0], dai.UsbSpeed.HIGH) as device:
      print("Available camera sensors: ", device.getCameraSensorNames())
      print("Usb speed: ", device.getUsbSpeed())
      calib = device.readCalibration()
      eeprom = calib.getEepromData()

    
      print(f"Product name: {eeprom.productName}, board name {eeprom.boardName}")
      print(f"Board revision: {eeprom.boardRev}")
if __name__ == "__main__":
    main()
