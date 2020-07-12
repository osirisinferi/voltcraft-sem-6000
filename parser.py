from message import *

class InvalidPayloadLengthException(Exception):
    def __init__(self, message_class, expected_payload_length, actual_payload_length):
        self.message_class = message_class
        self.expected_payload_length = expected_payload_length
        self.actual_payload_length = actual_payload_length

    def __str__(self):
        return "message has invalid payload length for " + self.message_class.__name__ +  " (expected: " + str(self.expected_payload_length) + ", actual=" + str(self.actual_payload_length) + ")"

class MessageParser:
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

    def parse(self, data):
        payload = self._parse_payload(data)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x00':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=AuthenticationNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return AuthorizationNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x01':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=ChangePinNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True
            
            return ChangePinNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x02':
            if len(payload) != 5:
                raise InvalidPayloadLengthException(message_class=ResetPinNotification.__class__, expected_payload_length=5, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return ResetPinNotification(was_successful=was_successful)

        if payload[0:2] == b'\x03\x00':
            if len(payload) != 3:
                raise InvalidPayloadLengthException(message_class=PowerSwitchNotification.__class__, expected_payload_length=3, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return PowerSwitchNotification(was_successful=was_successful)

        if payload[0:3] == b'\x0f\x00\x05':
            if len(payload) != 4:
                raise InvalidPayloadLengthException(message_class=LEDSwitchNotification.__class__, expected_payload_length=4, actual_payload_length=len(payload))

            return LEDSwitchNotification(was_successful=True)

        if payload[0:2] == b'\x01\x00':
            if len(payload) != 3:
                raise InvalidPayloadLengthException(message_class=SynchronizeDateAndTimeNotification.__class__, expected_payload_length=3, actual_payload_length=len(payload))

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return SynchronizeDateAndTimeNotification(was_successful=was_successful)

        if payload[0:2] == b'\x10\x00':
            if len(payload) != 13:
                raise InvalidPayloadLengthException(message_class=RequestedSettingsNotification.__class__, expected_payload_length=13, actual_payload_length=len(payload))

            is_reduced_mode_active = False
            if payload[2:3] == b'\x01':
                is_reduced_mode_active = True

            normal_price_in_cent = int.from_bytes(payload[3:4], 'big')
            reduced_price_in_cent = int.from_bytes(payload[4:5], 'big')

            reduced_mode_start_in_minutes = int.from_bytes(payload[5:7], 'big')
            reduced_mode_end_in_minutes = int.from_bytes(payload[7:9], 'big')

            is_led_on = False
            if payload[9:10] == b'\x01':
                is_led_on = True

            power_limit_in_watt = int.from_bytes(payload[11:13], 'big')

            return RequestedSettingsNotification(is_reduced_mode_active=is_reduced_mode_active, normal_price_in_cent=normal_price_in_cent, reduced_price_in_cent=reduced_price_in_cent, reduced_mode_start_in_minutes=reduced_mode_start_in_minutes, reduced_mode_end_in_minutes=reduced_mode_end_in_minutes, is_led_on=is_led_on, power_limit_in_watt=power_limit_in_watt)

        raise Exception('Unsupported message')
