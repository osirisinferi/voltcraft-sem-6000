import datetime

class AbstractCommand:
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return True

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "()"


class AbstractSwitchCommand():
    def __init__(self, on):
        self.on = on

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.on != other.on:
            return False

        return True

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(on=" + str(self.on) + ")"


class AbstractCommandConfirmationNotification:
    def __init__(self, was_successful):
        self.was_successful = was_successful

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.was_successful != other.was_successful:
            return False

        return True

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(was_successful=" + str(self.was_successful) + ")"


class AuthorizeCommand():
    def __init__(self, pin):
        self.pin = pin

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.pin != other.pin:
            return False

        return True

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(pin=" + str(self.pin) + ")"


class ChangePinCommand():
    def __init__(self, pin, new_pin):
        self.pin = pin
        self.new_pin = new_pin

    def __eq__(self, other):
        if not isinstance(other, self__class__):
            return False

        if self.pin != other.pin:
            return False

        if self.new_pin != other.new_pin:
            return False

        return True

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(pin=" + str(self.pin) + ", new_pin=" + str(self.new_pin) + ")"


class ResetPinCommand(AbstractCommand):
    pass

class PowerSwitchCommand(AbstractSwitchCommand):
    pass

class LEDSwitchCommand(AbstractSwitchCommand):
    pass

class SynchronizeDateAndTimeCommand():
    def __init__(self, year, month, day, hour, minute, second):
        d = datetime.datetime(year, month, day, hour, minute, second)

        self.year = d.year
        self.month = d.month
        self.day = d.day

        self.hour = d.hour
        self.minute = d.minute
        self.second = d.second

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.year != other.year:
            return False

        if self.month!= other.month:
            return False

        if self.day != other.day:
            return False

        if self.hour != other.hour:
            return False

        if self.minute != other.minute:
            return False

        if self.second != other.second:
            return False

        return True

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(year=" + str(self.year) + ", month=" + str(self.month) + ", day=" + str(self.day) + ", hour=" + str(self.hour) + ", minute=" + str(self.minute) + ", second=" + str(self.second) + ")"


class AuthorizationNotification(AbstractCommandConfirmationNotification):
    pass

class ChangePinNotification(AbstractCommandConfirmationNotification):
    pass

class ResetPinNotification(AbstractCommandConfirmationNotification):
    pass

class PowerSwitchNotification(AbstractCommandConfirmationNotification):
    pass

class LEDSwitchNotification(AbstractCommandConfirmationNotification):
    pass

class SynchronizeDateAndTimeNotification(AbstractCommandConfirmationNotification):
    pass
