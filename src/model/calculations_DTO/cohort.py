from model.calculations_DTO.calculated_parameter import CalculatedParameter
from typing import List, Tuple


class Cohort:

    def __init__(
        self,
        time_period_start,
        time_period_end,
        number_of_items=0,
        number_of_failures=0,
    ):
        self.time_period_start = time_period_start
        self.time_period_end = time_period_end
        self.number_of_items = number_of_items
        self.number_of_failures = number_of_failures

    def add_item(self):
        self.number_of_items += 1

    def add_failure(self):
        self.number_of_failures += 1

    def set_defect_intensity(self, defect_intensity: CalculatedParameter):
        self.defect_intensity = defect_intensity
