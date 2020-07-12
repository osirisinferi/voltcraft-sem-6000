import unittest

from encoder import MessageEncoder
from parser import MessageParser
from message import *

class MessagesTest(unittest.TestCase):
    def test_AuthorizationNotification(self):
        command = AuthorizationNotification(True)
        message = MessageEncoder().encode(command)
        parsed_command = MessageParser().parse(message)

        self.assertEqual(command, parsed_command)

    def test_ChangePinNotification(self):
        command = ChangePinNotification(True)
        message = MessageEncoder().encode(command)
        parsed_command = MessageParser().parse(message)

        self.assertEqual(command, parsed_command)

    def test_ResetPinNotification(self):
        command = ResetPinNotification(True)
        message = MessageEncoder().encode(command)
        parsed_command = MessageParser().parse(message)

        self.assertEqual(command, parsed_command)

    def test_PowerSwitchNotification(self):
        command = PowerSwitchNotification(True)
        message = MessageEncoder().encode(command)
        parsed_command = MessageParser().parse(message)

        self.assertEqual(command, parsed_command)

    def test_LEDSwitchNotification(self):
        command = LEDSwitchNotification(True)
        message = MessageEncoder().encode(command)
        parsed_command = MessageParser().parse(message)

        self.assertEqual(command, parsed_command)


