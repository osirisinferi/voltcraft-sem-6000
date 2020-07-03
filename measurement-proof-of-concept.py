from bluepy import btle
import sys

def _create_command_message(payload):
    command = b'\x0f'
    
    command += (len(payload)+1).to_bytes(1, 'little')
    command += payload
    
    command += ((1+sum(payload)) & 0xff).to_bytes(1, 'little')
    command += b'\xff\xff'
    
    return command

class SEM6000Delegate(btle.DefaultDelegate):
    def handleNotification(self, cHandle, data):
        print("received data from handle " + str(cHandle) + ": " + str(data), file=sys.stderr)


pin = b'0000'
device_address = '18:62:e4:12:41:ae'

delegate = SEM6000Delegate()
peripheral = btle.Peripheral(deviceAddr=device_address).withDelegate(delegate)
characteristic = peripheral.getCharacteristics(uuid='0000fff3-0000-1000-8000-00805f9b34fb')[0]

authorize_command = _create_command_message(b'\x17\x00\x00' + pin + b'\x00\x00\x00\x00')
characteristic.write(authorize_command)
peripheral.waitForNotifications(10)

capture_measurement_command = _create_command_message(b'\x04\x00\x00\x00\x05')
while True:
    characteristic.write(capture_measurement_command)
    peripheral.waitForNotifications(10)


