from model.valve_execution_type_enum import ValveExecutionType
from model.valve_function_type_enum import ValveFunctionType
from model.failure_type_enum import FailureType
from model.analysis_result import AnalysisResult
from typing import List


class Analysis:

    def __init__(
        self,
        name,
        valve_execution_type: ValveExecutionType,
        valve_function_type: ValveFunctionType,
        failure_type: FailureType,
        operating_time_array: List[int],
        confidence_level: float,
        standard_intensity: float,
        number_of_intervals: int,
        observation_period: int,
        operating_time_exceeds_observation: bool,
    ):
        self.name = name
        self.valve_execution_type = valve_execution_type
        self.valve_function_type = valve_function_type
        self.failure_type = failure_type
        self.operating_time_array = operating_time_array
        self.confidence_level = confidence_level
        self.standard_intensity = standard_intensity
        self.number_of_intervals = number_of_intervals
        self.observation_period = observation_period
        self.operating_time_exceeds_observation = operating_time_exceeds_observation

        self.operating_times_array = None

    def set_operating_times_array(self, operating_times_array: List[int]):
        self.operating_times_array = operating_times_array

    def set_number_of_items(self, number_of_items):
        self.number_of_items = number_of_items

    def add_analysis_result(self, analysis_result: AnalysisResult):
        self.analysis_result = analysis_result
