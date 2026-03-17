from src.model.calculations_DTO.calculated_parameter import CalculatedParameter
from typing import List


class CalculatedParameterArray:

    def __init__(self, name=""):
        self.array = []

    def append_value_to_array(self, value):
        if type(value) == CalculatedParameter:
            self.array.append(value)
        else:
            self.array.append(CalculatedParameter(value))

    def get_values(self):
        return [i.value for i in self.array]

    def set_plot_config(self, color, grayscale_color, label, linestyle):
        self.color = color
        self.grayscale_color = grayscale_color
        self.label = label
        self.linestyle = linestyle
