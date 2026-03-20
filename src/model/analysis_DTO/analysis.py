from model.calculations_DTO.calculated_parameter import CalculatedParameter
from model.calculations_DTO.cohort import Cohort
from typing import List, Tuple


class Analysis:

    def __init__(
        self,
        observation_period_beginning,
        observation_period_end,
        number_of_semiperiods,
        number_of_cohorts,
    ):
        self.observation_period_beginning = observation_period_beginning
        self.observation_period_end = observation_period_end
        self.number_of_semiperiods = number_of_semiperiods
        self.number_of_cohorts = number_of_cohorts

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
