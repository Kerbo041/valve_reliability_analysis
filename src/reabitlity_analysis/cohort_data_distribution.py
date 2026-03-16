from typing import List, Tuple
from datetime import datetime
from model.calculations_DTO.cohort import Cohort


def distribute_data_across_cohorts(
    self,
    observation_period_beginning,
    observation_period_end,
    number_of_semiperiods,
    number_of_cohorts,
    analysis_data_set: List[Tuple[datetime, List[datetime]]],
):
    semiperiod_delta_time = (
        observation_period_end - observation_period_beginning
    ) / number_of_semiperiods
    semiperiods_time_stamps_array = [
        observation_period_beginning + semiperiod_delta_time * i
        for i in range(number_of_semiperiods)
    ]
    max_item_operating_time = (
        max(analysis_data_set, key=lambda x: x[0]) - observation_period_end
    )
    min_item_operating_time = (
        min(analysis_data_set, key=lambda x: x[0]) - observation_period_beginning
    )

    cohort_delta_time = (
        max_item_operating_time - min_item_operating_time
    ) / number_of_cohorts

    cohort_time_stamps_array = [
        min_item_operating_time + cohort_delta_time * i
        for i in range(number_of_cohorts)
    ]

    cohorts_array = [
        Cohort(cohort_time_stamps_array[i], cohort_time_stamps_array[i + 1])
        for i in cohort_time_stamps_array
    ]

    for semiperiod_index in range(number_of_semiperiods) - 1:
        current_semiperiod_start = semiperiods_time_stamps_array[semiperiod_index]
        current_semiperiod_end = semiperiods_time_stamps_array[semiperiod_index + 1]
        average_semiperiod_time = (
            current_semiperiod_end - current_semiperiod_start
        ) / 2 + current_semiperiod_start

        for item in analysis_data_set:
            item_operating_time = item[0] - average_semiperiod_time
            item_failures_time_array = item[1]
            cohort_index = find_index_in_timestamps(
                item_operating_time, cohort_time_stamps_array
            )
            cohorts_array[cohort_index].add_item()
            for failure_time in item_failures_time_array:
                if current_semiperiod_end > failure_time > current_semiperiod_start:
                    cohorts_array[cohort_index].add_failure()
    return cohorts_array


def find_index_in_timestamps(item, timestamps_array):
    for i in timestamps_array:
        if timestamps_array[i] > item > timestamps_array[i + 1]:
            return i
