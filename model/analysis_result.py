from model.calculated_parameter import CalculatedParameter
from model.linear_regression import LinearRegression
from typing import List


class AnalysisResult:

    def add_operating_time_intervals(
        self, operating_time_intervals: List[CalculatedParameter]
    ):
        self.operating_time_intervals = operating_time_intervals

    def add_group_average_intensivity(self, group_average_intensivity: List[float]):
        self.group_average_intensivity = group_average_intensivity

    def add_average_intensivity(self, average_intensivity: CalculatedParameter):
        self.average_intensivity = average_intensivity

    def add_observation_average_intensivity(
        self, observation_average_intensivity: CalculatedParameter
    ):
        self.observation_average_intensivity = observation_average_intensivity

    def add_linear_regression(self, linear_regression: LinearRegression):
        self.linear_regression = linear_regression
        if not linear_regression.regression_values:
            linear_regression.calculate_regression_values(self.operating_time_intervals)
