#!/usr/bin/python3

import sys
from bluepy import btle

class AuthorizationNotification:
    def __init__(self, was_successful):
        self.was_successful = was_successful

    def __str__(self):
        return "AuthorizationNotification(was_successful=" + str(self.was_successful) + ")"

class SEM6000Delegate(btle.DefaultDelegate):
    def __init__(self, is_debug=False):
        btle.DefaultDelegate.__init__(self)

        self.is_debug = False
        if is_debug:
            self.is_debug = True

        self.last_notification = None

    def _parse_payload(self, data):
        if data[0:1] != b'\x0f':
            raise Exception("Invalid response")

        length_of_payload = data[1]

        payload = data[2:2+length_of_payload-1]
        checksum_received = data[2+length_of_payload-1]

        checksum = (1+sum(payload)) & 0xff

        if checksum_received != checksum:
            raise Exception("Invalid checksum " + str(checksum) + ", expected=" + str(checksum_received))

        if len(data) > 2+length_of_payload:
            # if suffix exists it must be b'\xff\xff'
            suffix = data[2+length_of_payload:]
            if suffix != b'\xff\xff':
                raise Exception("Invalid suffix " + str(suffix))

        return payload

    def _parse_notification(self, data):
        payload = self._parse_payload(data)

        if payload[0:2] == b'\x17\x00':
            if len(payload) != 5:
                raise Exception("invalid payload length for AuthenticationNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return AuthorizationNotification(was_successful=was_successful)

        return None

    def handleNotification(self, cHandle, data):
        if self.is_debug:
            print("received data from handle " + str(cHandle) + ": " + str(data), file=sys.stderr)

        self.last_notification = self._parse_notification(data)

        if self.is_debug:
            if not self.last_notification is None:
                print(self.last_notification, file=sys.stderr)
            else:
                print("Unknown notification received", file=sys.stderr)


class SEM6000():
    def __init__(self, deviceAddr=None, pin=None, iface=None):
        self.timeout = 10

        self.pin = b'0000'
        if not pin is None:
            self.pin = b''
            for i in pin:
                self.pin += int(i).to_bytes(1, 'little')

        self._delegate = SEM6000Delegate(is_debug=True)
        self._peripheral = btle.Peripheral(deviceAddr=deviceAddr, addrType=btle.ADDR_TYPE_PUBLIC, iface=iface).withDelegate(self._delegate)
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
        notification = self._delegate.last_notification

        if not isinstance(notification, AuthorizationNotification) or not notification.was_successful:
            raise Exception("Authentication failed")

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

