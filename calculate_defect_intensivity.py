from output_statistic_analyzis_to_csv import output_statistic_analyzis_to_csv
from model.analysis_result import Analysis
from model.valve_execution_type_enum import ValveExecutionType
from model.valve_function_type_enum import ValveFunctionType
from model.failure_type_enum import FailureType
from model.analysis_DTO.linear_regression import LinearRegression
from model.calculated_parameter import CalculatedParameter
from model.calculated_parameter_array import CalculatedParameterArray
import numpy as np
from scipy import stats
from typing import List, Tuple


def calculate_average_intensity(
    number_of_failures: int, number_of_items: int, period: int, name=""
):
    try:
        if period == 0 or number_of_items == 0:
            raise ZeroDivisionError
        if number_of_failures < 10:
            average_intensity = (2 * number_of_failures + 1) / (
                2 * number_of_items * period
            )
        else:
            average_intensity = number_of_failures / (number_of_items * period)
        return CalculatedParameter(name, average_intensity)
    except Exception as e:
        raise e


def calculate_confidence_interval_for_average_intensity(
    average_intensivity: CalculatedParameter,
    number_of_failures: int,
    confidence_level=0.9,
):
    try:
        # Квантили распределения хи-квадрат
        chi2_lower = stats.chi2.ppf((1 - confidence_level) / 2, 2 * number_of_failures)
        chi2_upper = stats.chi2.ppf((1 + confidence_level) / 2, 2 * number_of_failures)
        # Доверительные границы
        average_intensivity.set_lower_value(
            (average_intensivity.value * chi2_lower) / (2 * number_of_failures)
        )
        average_intensivity.set_upper_value(
            (average_intensivity.value * chi2_upper) / (2 * number_of_failures)
        )
    except Exception as e:
        raise e
        return None


def calculate_average_intensity_with_confidence_interval(
    number_of_failures: int,
    number_of_items: int,
    period: int,
    confidence_level=0.9,
    name="",
):
    average_intensity = calculate_average_intensity(
        number_of_failures, number_of_items, period, name
    )
    calculate_confidence_interval_for_average_intensity(
        average_intensity, number_of_failures, confidence_level
    )
    return average_intensity


class Cohort:

    def __init__(
        self,
        time_period_start,
        time_period_end,
        number_of_items=0,
        number_of_failrues=0,
    ):
        self.time_period_start = time_period_start
        self.time_period_end = time_period_end
        self.number_of_items = number_of_items
        self.number_of_failrues = number_of_failrues

    def set_defect_intensity(self, defect_intencity: CalculatedParameter):
        self.defect_intencity = defect_intencity


def get_analysis_result(
    cohorts_array: List[Cohort], subperiod_duration, confidence_level
):
    all_number_of_failrues = [cohort.number_of_failrues for cohort in cohorts_array]
    all_number_of_items = [cohort.number_of_items for cohort in cohorts_array]

    average_defect_intensivity = calculate_average_intensity_with_confidence_interval(
        all_number_of_failrues,
        all_number_of_items,
        subperiod_duration,
        confidence_level,
    )

    for cohort in cohorts_array:
        cohort_defect_intensivity = (
            calculate_average_intensity_with_confidence_interval(
                cohort.number_of_failrues,
                cohort.number_of_items,
                subperiod_duration,
                confidence_level,
            )
        )
        cohort.set_defect_intensity(cohort_defect_intensivity)

    return average_defect_intensivity


# def get_analysis_result(
#     # analysis: Analysis,  # Гад-object
#     groups: List[(Tuple)],
# ):
#     try:
#         # Предупреждение: рекомендуется не менее 50 значений для точного анализа
#         # Расчёт средней интенсивности отказов

#         number_of_failures = len(analysis.operating_time_array)

#         if not operating_period:
#             operating_period = max(analysis.operating_time_array)

#         analysis.add_average_intensity(
#             calculate_average_intensity_with_confidence_interval(
#                 number_of_failures,
#                 analysis.number_of_items,
#                 operating_period,
#                 analysis.confidence_level,
#                 "average_operating_failure_rate",
#             )
#         )
#         if analysis.operating_time_exceeds_observation:
#             analysis.add_observation_average_intensity(
#                 calculate_average_intensity_with_confidence_interval(
#                     number_of_failures,
#                     analysis.number_of_items,
#                     analysis.observation_period,
#                     analysis.confidence_level,
#                     "average_observation_failure_rate",
#                 )
#             )

#         # Создание интервалов
#         interval_width = (
#             max(analysis.operating_time_array) - min(analysis.operating_time_array)
#         ) / analysis.number_of_intervals
#         intervals_borders = np.linspace(
#             min(analysis.operating_time_array),
#             max(analysis.operating_time_array),
#             analysis.number_of_intervals + 1,
#         )
#         midpoints_of_intervals = (intervals_borders[:-1] + intervals_borders[1:]) / 2
#         analysis.add_operating_time_intervals(CalculatedParameterArray())
#         for i in range(analysis.number_of_intervals):
#             analysis.operating_time_intervals.append_value_to_array(
#                 CalculatedParameter(
#                     midpoints_of_intervals[i],
#                     f"interval {i + 1}",
#                     intervals_borders[i],
#                     intervals_borders[i + 1],
#                 )
#             )
#         # Подсчёт отказов в интервалах
#         count_of_failures_in_groups, _ = np.histogram(
#             analysis.operating_time_array, bins=intervals_borders
#         )

#         # Расчёт интенсивности отказов для каждого интервала
#         analysis.add_group_average_intensity(
#             CalculatedParameterArray("failure_rates_for_each_group")
#         )
#         for _count in count_of_failures_in_groups:
#             analysis.group_average_intensity.append_value_to_array(
#                 calculate_average_intensity_with_confidence_interval(
#                     _count,
#                     analysis.number_of_items,
#                     interval_width,
#                     analysis.confidence_level,
#                 )
#             )

#         # гамма-распределение
#         k, _, theta = stats.gamma.fit(analysis.operating_time_array, floc=0)
#         gamma_intensities = [
#             (
#                 stats.gamma.pdf(t, k, scale=theta)
#                 / (1 - stats.gamma.cdf(t, k, scale=theta))
#                 if (1 - stats.gamma.cdf(t, k, scale=theta)) > 0
#                 else 0
#             )
#             for t in midpoints_of_intervals
#         ]

#         # statistic = (
#         #     data,
#         #     number_of_items,
#         #     number_of_failures,
#         #     average_operating_failure_rate,
#         #     average_observation_failure_rate,
#         #     interval_width,
#         #     intervals_borders,
#         #     regression_line_slope,
#         #     regression_line_intercept,
#         #     failure_rates_for_each_group,
#         #     count - of_failures_in_groups,
#         #     midpoints_of_intervals,
#         #     сonfidence_interval_upper_border,
#         #     сonfidence_interval_lower_border,
#         #     chi2_сonfidence_interval_upper_border,
#         #     chi2_сonfidence_interval_lower_border,
#         #     avg_failure_rate_chi2_сonfidence_interval_lower_border,
#         #     avg_failure_rate_chi2_сonfidence_interval_upper_border,
#         #     avg_failure_rate_2_chi2_сonfidence_interval_lower_border,
#         #     avg_failure_rate_2_chi2_сonfidence_interval_upper_border,
#         #     p_value,
#         #     r_value,
#         # )
#         # output_statistic_analyzis_to_csv(
#         # )
#     except Exception as exception:
#         # print(output_file_path, exception)
#         pass
