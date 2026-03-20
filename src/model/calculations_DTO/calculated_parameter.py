class CalculatedParameter:

    def __init__(self, value, name="", lower_value=None, upper_value=None):
        if name:
            self.name = name
        self.value = value
        if lower_value:
            self.lower_value = lower_value
        if upper_value:
            self.upper_value = upper_value

    def set_lower_value(self, lower_value):
        self.lower_value = lower_value

    def set_upper_value(self, upper_value):
        self.upper_value = upper_value
