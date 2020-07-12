#!/usr/bin/python3

import binascii
import datetime
import sys
from bluepy import btle

import parser
import encoder
from message import *


class SEM6000Delegate(btle.DefaultDelegate):
    def __init__(self, debug=False):
        btle.DefaultDelegate.__init__(self)

        self.debug = False
        if debug:
            self.debug = True

        self.last_notification = None

        self._parser = parser.MessageParser()

    def handleNotification(self, cHandle, data):
        exception = None
        try:
            self.last_notification = self._parser.parse(data)
        except Exception as e:
            if self.debug:
                print("received data from handle " + str(cHandle) + ": " + str(binascii.hexlify(data)) + " (Unknown Notification)", file=sys.stderr)
            raise e

        if self.debug:
            print("received data from handle " + str(cHandle) + ": " + str(binascii.hexlify(data)) + " (" + str(self.last_notification) + ")", file=sys.stderr)


class SEM6000():
    def __init__(self, deviceAddr=None, pin=None, iface=None, debug=False):
        self.timeout = 10
        self.debug = debug

        self.pin = '0000'
        if not pin is None:
            self.pin = pin

        self._encoder = encoder.MessageEncoder()

        self._delegate = SEM6000Delegate(self.debug)
        self._peripheral = btle.Peripheral(deviceAddr=deviceAddr, addrType=btle.ADDR_TYPE_PUBLIC, iface=iface).withDelegate(self._delegate)
        self._characteristics = self._peripheral.getCharacteristics(uuid='0000fff3-0000-1000-8000-00805f9b34fb')[0]

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
        command = AuthorizeCommand(self.pin)
        self._send_command(command)
        notification = self._delegate.last_notification

        if not isinstance(notification, AuthorizationNotification) or not notification.was_successful:
            raise Exception("Authentication failed")

        return notification

    def change_pin(self, new_pin):
        command = ChangePinCommand(self.pin, new_pin)
        self._send_command(command)
        notification = self._delegate.last_notification

        if not isinstance(notification, ChangePinNotification) or not notification.was_successful:
            raise Exception("Change PIN failed")

        return notification

    def reset_pin(self):
        command = ResetPinCommand()
        self._send_command(command)
        notification = self._delegate.last_notification

        if not isinstance(notification, ResetPinNotification) or not notification.was_successful:
            raise Exception("Reset PIN failed")

        return notification

    def power_on(self):
        command = PowerSwitchCommand(True)
        self._send_command(command)
        notification = self._delegate.last_notification
        
        if not isinstance(notification, PowerSwitchNotification) or not notification.was_successful:
            raise Exception("Power on failed")

        return notification

    def power_off(self):
        command = PowerSwitchCommand(False)
        self._send_command(command)
        notification = self._delegate.last_notification
        
        if not isinstance(notification, PowerSwitchNotification) or not notification.was_successful:
            raise Exception("Power off failed")

        return notification

    def led_on(self):
        command = LEDSwitchCommand(True)
        self._send_command(command)
        notification = self._delegate.last_notification
        
        if not isinstance(notification, LEDSwitchNotification) or not notification.was_successful:
            raise Exception("LED on failed")

        return notification

    def led_off(self):
        command = LEDSwitchCommand(False)
        self._send_command(command)
        notification = self._delegate.last_notification
        
        if not isinstance(notification, LEDSwitchNotification) or not notification.was_successful:
            raise Exception("LED off failed")

        return notification

    def synchronize_date_and_time(self, isodatetime):
        date_and_time = datetime.datetime.fromisoformat(isodatetime)
        command = SynchronizeDateAndTimeCommand(date_and_time.year, date_and_time.month, date_and_time.day, date_and_time.hour, date_and_time.minute, date_and_time.second)
        self._send_command(command)
        notification = self._delegate.last_notification

        if not isinstance(notification, SynchronizeDateAndTimeNotification) or not notification.was_successful:
            raise Exception("Synchronize date and time failed")

        return notification

    def request_settings(self):
        command = RequestSettingsCommand()
        self._send_command(command)
        notification = self._delegate.last_notification

        if not isinstance(notification, RequestedSettingsNotification):
            raise Exception("Request settings failed")

        return notification

    def _send_command(self, command):
        encoded_command = self._encoder.encode(command)

        if self.debug:
            print("sent data: " + str(binascii.hexlify(encoded_command)) + " (" + str(command) + ")", file=sys.stderr)

        self._characteristics.write(encoded_command)
        self._peripheral.waitForNotifications(self.timeout)

def _format_minutes_as_time(minutes):
    hour = minutes // 24
    minute = minutes - hour*60

    return "{:02}:{:02}".format(hour, minute)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        devices = SEM6000.discover()
        for device in devices:
            print(device['name'] + '\t' + device['address'])
    else:
        deviceAddr = sys.argv[1]
        pin = sys.argv[2]
        cmd = sys.argv[3]

        sem6000 = SEM6000(deviceAddr, pin, debug=True)

        if cmd != 'reset_pin':
            sem6000.authorize()

        if cmd == 'change_pin':
            sem6000.change_pin(sys.argv[4])
        if cmd == 'reset_pin':
            sem6000.reset_pin()
        if cmd == 'power_on':
            sem6000.power_on()
        if cmd == 'power_off':
            sem6000.power_off()
        if cmd == 'led_on':
            sem6000.led_on()
        if cmd == 'led_off':
            sem6000.led_off()
        if cmd == 'synchronize_date_and_time':
            sem6000.synchronize_date_and_time(sys.argv[4])
        if cmd == 'request_settings':
            response = sem6000.request_settings()
            assert isinstance(response, RequestedSettingsNotification)

            print("Settings:")
            if response.is_reduced_mode_active:
                print("\tReduced mode:\t\tOn")
            else:
                print("\tReduced mode:\t\tOff")

            print("\tNormal price:\t\t{:.2f} EUR".format(response.normal_price_in_cent/100))
            print("\tReduced price:\t\t{:.2f} EUR".format(response.reduced_price_in_cent/100))

            print("\tRecuced mode start:\t{} minutes ({})".format(response.reduced_mode_start_in_minutes, _format_minutes_as_time(response.reduced_mode_start_in_minutes)))
            print("\tRecuced mode end:\t{} minutes ({})".format(response.reduced_mode_end_in_minutes, _format_minutes_as_time(response.reduced_mode_end_in_minutes)))

            if response.is_led_on:
                print("\tLED state;\t\tOn")
            else:
                print("\tLED state;\t\tOff")

            print("\tPower limit:\t\t{} W".format(response.power_limit_in_watt))

