from model.calculations_DTO.calculated_parameter import CalculatedParameter
from model.calculations_DTO.cohort import Cohort
from typing import List, Tuple
from src.model.analysis_DTO.filter_parameters import FilterParameters
from src.model.analysis_DTO.analysis_parameters import AnalysisParameters


class Analysis:

    def __init__(
        self,
        filter_parameters: FilterParameters,
        analysis_parameters: AnalysisParameters,
    ):
        self.filter_parameters = filter_parameters
        self.analysis_parameters = analysis_parameters

    def get_observation_parameters(self):
        return (
            self.observation_period_beginning,
            self.observation_period_end,
            self.number_of_semiperiods,
            self.number_of_cohorts,
        )

    def add_cohorts(self, cohorts_array: List[Cohort]):
        self.cohorts_array = cohorts_array

    def add_analysis_result(
        self,
    ):
        pass
