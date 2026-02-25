from model.calculated_parameter import CalculatedParameter
from model.calculated_parameter_array import CalculatedParameterArray
from model.linear_regression import LinearRegression
from model.analysis_group import AnalysisGroup
from typing import List
from datetime import datetime


class AnalysisResult:

    def __init__(
        self,
        analysis_groups: List[AnalysisGroup],
        linear_regression: LinearRegression,
        observation_period_start: datetime,
        observation_period_end: datetime,
        confidence_level: float,
        number_of_intervals: int,
        standard_intensity: float,
        description: str,
    ):
        self.analysis_groups = analysis_groups
        self.linear_regression = linear_regression
        self.observation_period_start = observation_period_start
        self.observation_period_end = observation_period_end
        self.confidence_level = confidence_level
        self.standard_intensity = standard_intensity
        self.number_of_intervals = number_of_intervals
        self.description = description
