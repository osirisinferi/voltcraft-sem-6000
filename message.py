class AbstractSwitchCommand:
    def __init__(self, on):
        self.on = on

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(on=" + str(self.on) + ")"


class AbstractCommandConfirmationNotification:
    def __init__(self, was_successful):
        self.was_successful = was_successful

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(was_successful=" + str(self.was_successful) + ")"


class AuthorizeCommand():
    def __init__(self, pin):
        self.pin = pin

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(pin=" + str(self.pin) + ")"

class ChangePinCommand():
    def __init__(self, pin, new_pin):
        self.pin = pin
        self.new_pin = new_pin

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(pin=" + str(self.pin) + ", new_pin=" + str(self.new_pin) + ")"

class PowerSwitchCommand(AbstractSwitchCommand):
    pass

class LEDSwitchCommand(AbstractSwitchCommand):
    pass


class AuthorizationNotification(AbstractCommandConfirmationNotification):
    pass

class ChangePinNotification(AbstractCommandConfirmationNotification):
    pass

class PowerSwitchNotification(AbstractCommandConfirmationNotification):
    pass

class LEDSwitchNotification(AbstractCommandConfirmationNotification):
    pass

