from model.calculations_DTO.calculated_parameter import CalculatedParameter
from model.calculations_DTO.calculated_parameter_array import CalculatedParameterArray
from model.calculations_DTO.cohort import Cohort
from typing import List
from scipy import stats
import numpy as np


def calculate_confidence_interval(
    time_array,
    values_array,
    regression_line_values,
    number_of_cohorts,
    confidence_level,
):
    if type(regression_line_values) == List[CalculatedParameter]:
        # Доверительный интервал линейной регрессии
        # Дисперсия независимой переменной (времени)
        variance_of_midpoints = np.var(time_array)
        # Квадраты ошибок (разница между предсказанными и фактическими значениями)
        squared_errors = (
            np.array([i.value for i in regression_line_values]) - values_array
        ) ** 2
        # Остаточная дисперсия (оценка дисперсии ошибок)
        residual_variance = sum(squared_errors) / (number_of_cohorts - 2)
        # Дисперсия предсказанных значений для каждой точки
        prediction_variance = residual_variance * (
            1
            + 1 / number_of_cohorts
            + (time_array - np.mean(time_array)) ** 2 / variance_of_midpoints
        )
        # Стандартная ошибка предсказания
        prediction_std_error = np.sqrt(prediction_variance)
        # Критерий t-распределения
        t_value = stats.t.ppf((1 + confidence_level) / 2, df=number_of_cohorts - 2)
        # Границы доверительного интервала
        for i in regression_line_values:
            i.set_lower(i.value - t_value * prediction_std_error)
            i.set_upper(i.value + t_value * prediction_std_error)


def is_trend_significant(
    time_array,
    values_array,
    regression_line_values,
    number_of_cohorts,
    confidence_level,
):
    # Доверительный интервал линейной регрессии
    # Дисперсия независимой переменной (времени)
    variance_of_midpoints = np.var(time_array)
    # Квадраты ошибок (разница между предсказанными и фактическими значениями)
    squared_errors = (
        np.array([i.value for i in regression_line_values]) - values_array
    ) ** 2
    # Остаточная дисперсия (оценка дисперсии ошибок)
    residual_variance = sum(squared_errors) / (number_of_cohorts - 2)
    # гипотеза об отсутствии тренда
    mean_predictor_value = sum(time_array) / len(time_array)
    squared_deviations_from_mean = (time_array - mean_predictor_value) ** 2

    # Sa = (s2_T_FR * [i**2 for i in failure_rates] / (2 * sum(d_i2))) ** (1/2)
    slope_standard_error = np.sqrt(
        residual_variance / sum(squared_deviations_from_mean)
    )
    relative_slope_error = slope_standard_error / abs(
        np.array([i.value for i in regression_line_values])
    )
    prediction_variance = residual_variance * (
        1
        + 1 / number_of_cohorts
        + (time_array - np.mean(time_array)) ** 2 / variance_of_midpoints
    )
    # Стандартная ошибка предсказания
    prediction_std_error = np.sqrt(prediction_variance)
    # Критерий t-распределения
    t_value = stats.t.ppf((1 + confidence_level) / 2, df=number_of_cohorts - 2)
    is_trend_non_significant = relative_slope_error > t_value


def calculate_regression_line(
    self, cohorts_array: List[Cohort], number_of_cohorts, confidence_level
):
    time_array = [
        ((item.time_period_end - item.time_period_start) / 2) for item in cohorts_array
    ]
    values_array = [item.defect_intensity for item in cohorts_array]

    (
        regression_line_slope,
        regression_line_intercept,
        r_value,
        p_value,
        std_err,
    ) = stats.linregress(time_array, values_array)

    regression_line_values = [
        CalculatedParameter(item * regression_line_slope + regression_line_intercept)
        for item in time_array
    ]
    calculate_confidence_interval(
        time_array, values_array, number_of_cohorts, confidence_level
    )
    return (
        regression_line_values,
        regression_line_slope,
        regression_line_intercept,
        r_value,
        p_value,
    )
