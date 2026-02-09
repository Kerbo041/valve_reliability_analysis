from model.calculated_parameter import CalculatedParameter
from typing import List


class LinearRegression:

    def __init__(self, slope, intersept, time_values=None, regression_values=None):
        self.slope = slope
        self.intersept = intersept
        if time_values and type(time_values) == List[CalculatedParameter]:
            self.time_values = time_values
        else:
            self.time_values = None
        if regression_values and type(regression_values) == CalculatedParameter:
            self.regression_values = regression_values
        else:
            self.regression_values = None

    def calculate_regression_values(self, time_values):
        if time_values and type(time_values) == List[CalculatedParameter]:
            self.regression_values = [
                self.slope * i.value + self.intersept for i in time_values
            ]
