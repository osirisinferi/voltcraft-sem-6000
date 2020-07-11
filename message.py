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

