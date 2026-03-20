from datetime import datetime
from typing import List, Tuple

if __name__ == "__main__":
    import sys, os

    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
from src.reabitlity_analysis.cohort_data_distribution import (
    distribute_data_across_cohorts,
)
from src.reabitlity_analysis.defect_intensivity_calculation import get_analysis_result


def make_analysis(
    observation_period_beginning,
    observation_period_end,
    number_of_semiperiods,
    number_of_cohorts,
    analysis_data_set: List[Tuple[datetime, List[datetime]]],
    confidence_level=0.9,
):
    cohorts_array = distribute_data_across_cohorts(
        observation_period_beginning,
        observation_period_end,
        number_of_semiperiods,
        number_of_cohorts,
        analysis_data_set,
    )
    subperiod_duration = (
        observation_period_end - observation_period_beginning
    ).days / number_of_semiperiods
    analysis_result = get_analysis_result(
        cohorts_array, subperiod_duration, confidence_level
    )
    return analysis_result, cohorts_array


if __name__ == "__main__":
    time_format = "%d.%m.%Y"

    # analysis parameters
    observation_period_beginning = datetime.strptime("01.01.2000", time_format)
    observation_period_end = datetime.strptime("01.01.2010", time_format)
    number_of_semiperiods = 10
    number_of_cohorts = 10
    # data generation parameters
    number_of_items = 100
    max_number_of_failures_per_item = 10
    items_start_datetime = datetime.strptime("01.01.1970", time_format)
    items_end_datetime = datetime.strptime("01.01.2000", time_format)
    # data creation
    analysis_data_set = []
    from random import random, randint

    for i in range(number_of_items):
        item_datetime = (
            items_start_datetime
            + (items_end_datetime - items_start_datetime) * random()
        )
        item_failures = [
            observation_period_beginning
            + (observation_period_end - observation_period_beginning) * random()
            for j in range(randint(0, max_number_of_failures_per_item))
        ]
        analysis_data_set.append((item_datetime, item_failures))
    analysis_result, cohorts_array = make_analysis(
        observation_period_beginning,
        observation_period_end,
        number_of_semiperiods,
        number_of_cohorts,
        analysis_data_set,
    )
    print(analysis_result.value)
    for i in cohorts_array:
        print(
            i.number_of_failures,
            i.number_of_items,
            i.time_period_start.days,
            i.time_period_end.days,
            i.defect_intensity.value,
        )
