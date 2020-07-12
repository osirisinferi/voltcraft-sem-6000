import message

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
                raise Exception("invalid payload length for AuthenticationNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return message.AuthorizationNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x01':
            if len(payload) != 5:
                raise Exception("invalid payload length for ChangePinNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True
            
            return message.ChangePinNotification(was_successful=was_successful)

        if payload[0:2] == b'\x17\x00' and payload[3:4] == b'\x02':
            if len(payload) != 5:
                raise Exception("invalid payload length for ResetPinNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return message.ResetPinNotification(was_successful=was_successful)

        if payload[0:2] == b'\x03\x00':
            if len(payload) != 3:
                raise Exception("invalid payload length for PowerSwitchNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return message.PowerSwitchNotification(was_successful=was_successful)

        if payload[0:3] == b'\x0f\x00\x05':
            if len(payload) != 4:
                raise Exception("invalid payload length for LEDSwitchNotification")

            return message.LEDSwitchNotification(was_successful=True)

        if payload[0:2] == b'\x01\x00':
            if len(payload) != 3:
                raise Exception("invalid payload length for SynchronizeDateAndTimeNotification")

            was_successful = False
            if payload[2:3] == b'\x00':
                was_successful = True

            return message.SynchronizeDateAndTimeNotification(was_successful=was_successful)

        return None
