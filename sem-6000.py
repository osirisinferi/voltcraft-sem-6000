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

    def discover(timeout=10):
        result = []

        scanner = btle.Scanner()
        scanner_results = scanner.scan(timeout)
        
        for device in scanner_results:
            address = device.addr
            # 0x02 - query "Incomplete List of 16-bit Service Class UUIDs"
            service_class_uuids = device.getValueText(2)
            # 0x09 - query complete local name
            complete_local_name = device.getValueText(9)

            if not service_class_uuids == "0000fff0-0000-1000-8000-00805f9b34fb":
                # not a sem6000 device
                continue

            result.append({'address': address, 'name': complete_local_name})

        return result

    def authorize(self):
        command = self._create_authorize_command()
        self._send_command(command)

    def power_on(self):
        command = self._create_power_on_command()
        self._send_command(command)

    def power_off(self):
        command = self._create_power_off_command()
        self._send_command(command)

    def led_on(self):
        command = self._create_led_on_command()
        self._send_command(command)

    def led_off(self):
        command = self._create_led_off_command()
        self._send_command(command)

    def _send_command(self, command):
        self._characteristics.write(command)
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

    def _create_led_on_command(self):
        return self._create_command_message(b'\x0f\x00\x05\x01' + b'\x00\x00\x00\x00')
 
    def _create_led_off_command(self):
        return self._create_command_message(b'\x0f\x00\x05\x00' + b'\x00\x00\x00\x00')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        devices = SEM6000.discover()
        for device in devices:
            print(device)
    else:
        deviceAddr = sys.argv[1]
        pin = sys.argv[2]
        cmd = sys.argv[3]

        sem6000 = SEM6000(deviceAddr, pin)
        if cmd == 'power_on':
            sem6000.power_on()
        if cmd == 'power_off':
            sem6000.power_off()
        if cmd == 'led_on':
            sem6000.led_on()
        if cmd == 'led_off':
            sem6000.led_off()

