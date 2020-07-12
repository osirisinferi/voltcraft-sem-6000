import unittest

from encoder import MessageEncoder
from parser import MessageParser
from message import *

class MessagesTest(unittest.TestCase):
    def test_AuthorizationNotification(self):
        message = AuthorizationNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_ChangePinNotification(self):
        message = ChangePinNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_ResetPinNotification(self):
        message = ResetPinNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_PowerSwitchNotification(self):
        message = PowerSwitchNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_LEDSwitchNotification(self):
        message = LEDSwitchNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_SynchroizeDateAndTimeNotification(self):
        message = SynchronizeDateAndTimeNotification(was_successful=True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.was_successful, 'was_successful value differs')

    def test_RequestedSettingsNotification(self):
        message = RequestedSettingsNotification(is_reduced_mode_active=True, normal_price_in_cent=100, reduced_price_in_cent=50, reduced_mode_start_in_minutes=1320, reduced_mode_end_in_minutes=300, is_led_active=True, power_limit_in_watt=500)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(True, parsed_message.is_reduced_mode_active, 'reduced_mode_is_active value differs')
        self.assertEqual(100, parsed_message.normal_price_in_cent, 'normal_price_in_cent value differs')
        self.assertEqual(50, parsed_message.reduced_price_in_cent, 'reduced_price value_in_cent differs')
        self.assertEqual(1320, parsed_message.reduced_mode_start_in_minutes, 'reduced_mode_start_in_minutes value differs')
        self.assertEqual(300, parsed_message.reduced_mode_end_in_minutes, 'reduced_mode_end_in_minutes value differs')
        self.assertEqual(True, parsed_message.is_led_active, 'is_led_active value differs')
        self.assertEqual(500, parsed_message.power_limit_in_watt, 'power_limit_in_watt value differs')

