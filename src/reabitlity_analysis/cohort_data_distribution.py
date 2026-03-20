from typing import List, Tuple
from datetime import datetime
import sys
import os

if __name__ == "__main__":
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    )
from src.model.calculations_DTO.cohort import Cohort


def distribute_data_across_cohorts(
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
        observation_period_end - min(analysis_data_set, key=lambda x: x[0])[0]
    )
    min_item_operating_time = (
        observation_period_beginning - max(analysis_data_set, key=lambda x: x[0])[0]
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
        for i in range(len(cohort_time_stamps_array) - 1)
    ]

    for semiperiod_index in range(number_of_semiperiods - 1):
        current_semiperiod_start = semiperiods_time_stamps_array[semiperiod_index]
        current_semiperiod_end = semiperiods_time_stamps_array[semiperiod_index + 1]
        average_semiperiod_time = (
            current_semiperiod_end - current_semiperiod_start
        ) / 2 + current_semiperiod_start

        for item in analysis_data_set:
            item_operating_time = average_semiperiod_time - item[0]
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
    for i in range(len(timestamps_array) - 1):
        if timestamps_array[i] <= item <= timestamps_array[i + 1]:
            return i
    return 0


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
    cohorts_array = distribute_data_across_cohorts(
        observation_period_beginning,
        observation_period_end,
        number_of_semiperiods,
        number_of_cohorts,
        analysis_data_set,
    )
    for i in analysis_data_set:
        print(i[0].strftime(time_format), end="|\t")
        for j in i[1]:
            print(j.strftime(time_format), end=", ")
        print("|")
    sum = 0
    for i in cohorts_array:
        print(
            i.number_of_failures,
            i.number_of_items,
            i.time_period_start.days,
            i.time_period_end.days,
        )
        sum += i.number_of_items
    print(sum)
