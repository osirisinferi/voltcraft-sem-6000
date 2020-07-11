import message

class CommandEncoder():
    def _encode_command_message(self, payload):
        command = b'\x0f'

        command += (len(payload)+1).to_bytes(1, 'little')
        command += payload

        command += ((1+sum(payload)) & 0xff).to_bytes(1, 'little')
        command += b'\xff\xff'

        return command

    def _encode_pin(self, pin):
            pin_bytes = b''
            for i in pin:
                pin_bytes += int(i).to_bytes(1, 'little')
            
            return pin_bytes

    def encode(self, command):
        if isinstance(command, message.AuthorizeCommand):
            encoded_pin = self._encode_pin(command.pin)
            return self._encode_command_message(b'\x17\x00\x00' + encoded_pin + b'\x00\x00\x00\x00')

        if isinstance(command, message.ChangePinCommand):
            encoded_pin = self._encode_pin(command.pin)
            encoded_new_pin = self._encode_pin(command.new_pin)
            return self._encode_command_message(b'\x17\x00\x01' + encoded_new_pin + encoded_pin)

        if isinstance(command, message.PowerSwitchCommand):
            if command.on:
                return self._encode_command_message(b'\x03\x00\x01' + b'\x00\x00')
            else:
                return self._encode_command_message(b'\x03\x00\x00' + b'\x00\x00')

        if isinstance(command, message.LEDSwitchCommand):
            if command.on:
                return self._encode_command_message(b'\x0f\x00\x05\x01' + b'\x00\x00\x00\x00')
            else:
                return self._encode_command_message(b'\x0f\x00\x05\x00' + b'\x00\x00\x00\x00')

        raise Exception('Unsupported command ' + str(command))

