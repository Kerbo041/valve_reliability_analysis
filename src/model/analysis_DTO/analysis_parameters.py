from typing import List, Dict, Tuple
from datetime import datetime


class AnalysisParameters:

    def __init__(
        self,
        observation_period_beginning: datetime,
        observation_period_end: datetime,
        number_of_semiperiods: int,
        number_of_cohorts: int,
    ):
        self.observation_period_beginning = observation_period_beginning
        self.observation_period_end = observation_period_end
        self.number_of_semiperiods = number_of_semiperiods
        self.number_of_cohorts = number_of_cohorts
