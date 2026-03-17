from src.reabitlity_analysis.linear_regression import calculate_regression_line
from src.model.calculations_DTO.calculated_parameter import CalculatedParameter
import numpy as np
from scipy import stats
from typing import List, Tuple
from model.calculations_DTO.cohort import Cohort


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


def get_analysis_result(
    cohorts_array: List[Cohort], subperiod_duration, confidence_level
):
    all_number_of_failrues = [cohort.number_of_failures for cohort in cohorts_array]
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
                cohort.number_of_failures,
                cohort.number_of_items,
                subperiod_duration,
                confidence_level,
            )
        )
        cohort.set_defect_intensity(cohort_defect_intensivity)

    return average_defect_intensivity
