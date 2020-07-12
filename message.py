import datetime

class AbstractCommand:
    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "()"


class AbstractSwitchCommand():
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

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(year=" + str(self.year) + ", month=" + str(self.month) + ", day=" + str(self.day) + ", hour=" + str(self.hour) + ", minute=" + str(self.minute) + ", second=" + str(self.second) + ")"


class RequestSettingsCommand(AbstractCommand):
    pass


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


class RequestedSettingsNotification:
    def __init__(self, is_reduced_mode_active, normal_price_in_cent, reduced_price_in_cent, reduced_mode_start_in_minutes, reduced_mode_end_in_minutes, is_led_on, power_limit_in_watt):
        self.is_reduced_mode_active = is_reduced_mode_active
        self.normal_price_in_cent = normal_price_in_cent
        self.self = self.reduced_price_in_cent = reduced_price_in_cent
        self.reduced_mode_start_in_minutes = reduced_mode_start_in_minutes
        self.reduced_mode_end_in_minutes = reduced_mode_end_in_minutes
        self.is_led_on = is_led_on
        self.power_limit_in_watt = power_limit_in_watt

    def __str__(self):
        command_name = self.__class__.__name__
        return command_name + "(is_reduced_mode_active=" + str(self.is_reduced_mode_active) + ", normal_price_in_cent=" + str(self.normal_price_in_cent) + ", reduced_price_in_cent=" + str(self.reduced_price_in_cent) + ", reduced_mode_start_in_minutes=" + str(self.reduced_mode_start_in_minutes) + ", reduced_mode_end_in_minutes=" + str(self.reduced_mode_end_in_minutes) + ", is_led_on=" + str(self.is_led_on) + ", power_limit_in_watt=" + str(self.power_limit_in_watt) + ")"

