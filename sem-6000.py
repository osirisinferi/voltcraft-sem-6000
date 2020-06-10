#!/usr/bin/python3

import sys
from bluepy import btle

class SEM6000():
    def __init__(self, deviceAddr=None, pin=None, iface=None):
        self.timeout = 10

        self.pin = b'0000'
        if not pin is None:
            self.pin = b''
            for i in pin:
                self.pin += int(i).to_bytes(1, 'little')

        self._peripheral = btle.Peripheral(deviceAddr=deviceAddr, addrType=btle.ADDR_TYPE_PUBLIC, iface=iface)
        self._characteristics = self._peripheral.getCharacteristics(uuid='0000fff3-0000-1000-8000-00805f9b34fb')[0]

        self.authorize()

    def authorize(self):
        authorize_command = self._create_authorize_command()
        self._characteristics.write(authorize_command)
        self._peripheral.waitForNotifications(self.timeout)

    def power_on(self):
        poweron_command = self._create_power_on_command()
        self._characteristics.write(poweron_command)
        self._peripheral.waitForNotifications(self.timeout)

    def power_off(self):
        poweroff_command = self._create_power_off_command()
        self._characteristics.write(poweroff_command)
        self._peripheral.waitForNotifications(self.timeout)

    def _create_command_message(self, payload):
        command = b'\x0f'

        command += (len(payload)+1).to_bytes(1, 'little')
        command += payload

        command += ((1+sum(payload)) & 0xff).to_bytes(1, 'little')
        command += b'\xff\xff'

        return command

    def _create_authorize_command(self):
        return self._create_command_message(b'\x17\x00\x00' + self.pin + b'\x00\x00\x00\x00')

    def _create_power_on_command(self):
        return self._create_command_message(b'\x03\x00\x01' + b'\x00\x00')
        
    def _create_power_off_command(self):
        return self._create_command_message(b'\x03\x00\x00' + b'\x00\x00')
 
if __name__ == '__main__':
    deviceAddr = sys.argv[1]
    pin = sys.argv[2]

    sem6000 = SEM6000(deviceAddr, pin)
    sem6000.power_off()
    sem6000.power_on()
    pass
