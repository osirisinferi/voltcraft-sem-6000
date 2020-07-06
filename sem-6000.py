#!/usr/bin/python3

import sys
from bluepy import btle

class AbstractCommandConfirmationNotification:
    def __init__(self, was_successful):
        self.was_successful = was_successful

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(was_successful=" + str(self.was_successful) + ")"
    

class AuthorizationNotification(AbstractCommandConfirmationNotification):
    pass

class ChangePinNotification(AbstractCommandConfirmationNotification):
    pass

class PowerSwitchNotification(AbstractCommandConfirmationNotification):
    pass

class LEDSwitchNotification(AbstractCommandConfirmationNotification):
    pass


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

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x00':
            if len(payload) != 5:
                raise Exception("invalid payload length for AuthenticationNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return AuthorizationNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x01':
            if len(payload) != 5:
                raise Exception("invalid payload length for ChangePinNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True
            
            return ChangePinNotification(was_successful=was_successful)

        if payload[0:2] == b'\x03\x00':
            if len(payload) != 3:
                raise Exception("invalid payload length for PowerSwitchNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return PowerSwitchNotification(was_successful=was_successful)

        if payload[0:3] == b'\x0f\x00\x05':
            if len(payload) != 4:
                raise Exception("invalid payload length for LEDSwitchNotification")

            return LEDSwitchNotification(was_successful=True)

        return None

    def handleNotification(self, cHandle, data):
        self.last_notification = self._parse_notification(data)

        if self.is_debug:
            if not self.last_notification is None:
                print("received data from handle " + str(cHandle) + ": " + str(data) + " (" + str(self.last_notification) + ")", file=sys.stderr)
            else:
                print("received data from handle " + str(cHandle) + ": " + str(data) + " (Unknown Notification)", file=sys.stderr)


class SEM6000():
    def __init__(self, deviceAddr=None, pin=None, iface=None, is_debug=False):
        self.timeout = 10
        self.is_debug = is_debug

        self.pin = b'0000'
        if not pin is None:
            self.pin = SEM6000.parse_pin_to_bytes(pin)

        self._delegate = SEM6000Delegate(self.is_debug)
        self._peripheral = btle.Peripheral(deviceAddr=deviceAddr, addrType=btle.ADDR_TYPE_PUBLIC, iface=iface).withDelegate(self._delegate)
        self._characteristics = self._peripheral.getCharacteristics(uuid='0000fff3-0000-1000-8000-00805f9b34fb')[0]

        self.authorize()

    def parse_pin_to_bytes(pin):
            pin_bytes = b''
            for i in pin:
                pin_bytes += int(i).to_bytes(1, 'little')
            
            return pin_bytes

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

    def change_pin(self, new_pin):
        new_pin_bytes = SEM6000.parse_pin_to_bytes(new_pin)
        
        command = self._create_change_pin_command(new_pin_bytes)
        self._send_command(command)
        notification = self._delegate.last_notification

        if not isinstance(notification, ChangePinNotification) or not notification.was_successful:
            raise Exception("Change PIN failed")

    def power_on(self):
        command = self._create_power_on_command()
        self._send_command(command)
        notification = self._delegate.last_notification
        
        if not isinstance(notification, PowerSwitchNotification) or not notification.was_successful:
            raise Exception("Power on failed")

    def power_off(self):
        command = self._create_power_off_command()
        self._send_command(command)
        notification = self._delegate.last_notification
        
        if not isinstance(notification, PowerSwitchNotification) or not notification.was_successful:
            raise Exception("Power off failed")

    def led_on(self):
        command = self._create_led_on_command()
        self._send_command(command)
        notification = self._delegate.last_notification
        
        if not isinstance(notification, LEDSwitchNotification) or not notification.was_successful:
            raise Exception("LED on failed")

    def led_off(self):
        command = self._create_led_off_command()
        self._send_command(command)
        notification = self._delegate.last_notification
        
        if not isinstance(notification, LEDSwitchNotification) or not notification.was_successful:
            raise Exception("LED off failed")


    def _send_command(self, command):
        if self.is_debug:
            print("sent data:" + str(command), file=sys.stderr)

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

    def _create_change_pin_command(self, new_pin_bytes):
        return self._create_command_message(b'\x17\x00\x01' + new_pin_bytes + self.pin)

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

        sem6000 = SEM6000(deviceAddr, pin, is_debug=True)

        if cmd == 'change_pin':
            sem6000.change_pin(sys.argv[4])
        if cmd == 'power_on':
            sem6000.power_on()
        if cmd == 'power_off':
            sem6000.power_off()
        if cmd == 'led_on':
            sem6000.led_on()
        if cmd == 'led_off':
            sem6000.led_off()

