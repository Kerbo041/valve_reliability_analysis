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
        standard_intensivity: float,
        observation_period: int,
    ):
        self.name = name
        self.valve_execution_type = valve_execution_type
        self.valve_function_type = valve_function_type
        self.failure_type = failure_type
        self.operating_time_array = operating_time_array
        self.standard_intensivity = standard_intensivity
        self.observation_period = observation_period

        self.operating_times_array = None

        self.analysis_result = AnalysisResult()
