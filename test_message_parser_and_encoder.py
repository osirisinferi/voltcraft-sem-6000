import unittest

from encoder import MessageEncoder
from parser import MessageParser
from message import *

class MessagesTest(unittest.TestCase):
    def test_AuthorizationNotification(self):
        message = AuthorizationNotification(True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(message, parsed_message)

    def test_ChangePinNotification(self):
        message = ChangePinNotification(True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(message, parsed_message)

    def test_ResetPinNotification(self):
        message = ResetPinNotification(True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(message, parsed_message)

    def test_PowerSwitchNotification(self):
        message = PowerSwitchNotification(True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(message, parsed_message)

    def test_LEDSwitchNotification(self):
        message = LEDSwitchNotification(True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(message, parsed_message)

    def test_SynchroizeDateAndTimeNotification(self):
        message = SynchronizeDateAndTimeNotification(True)
        encoded_message = MessageEncoder().encode(message)
        parsed_message = MessageParser().parse(encoded_message)

        self.assertEqual(message, parsed_message)
