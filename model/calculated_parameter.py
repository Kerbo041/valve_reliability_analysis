class CalculatedParameter:

    def __init__(self, name, value, lower_value, upper_value):
        self.name = name
        self.value = value

    def set_lower_value(self, lower_value):
        self.lower_value = lower_value

    def set_upper_value(self, upper_value):
        self.upper_value = upper_value
