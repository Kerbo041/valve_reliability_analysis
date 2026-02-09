from model.calculated_parameter import CalculatedParameter
from model.calculated_parameter_array import CalculatedParameterArray
from typing import List
from scipy import stats
import numpy as np


class LinearRegression:

    def __init__(self, slope, intersept, regression_values=None):
        self.slope = slope
        self.intersept = intersept

        if regression_values and type(regression_values) == CalculatedParameterArray:
            self.regression_line_values = regression_values
        else:
            self.regression_line_values = None

    def calculate_regression_values(self, time_array):
        self.regression_line_values = CalculatedParameterArray("regression_line_values")
        if time_array and type(time_array) == CalculatedParameterArray:
            for i in time_array:
                self.regression_line_values.append_value_to_array(
                    self.slope * i.value + self.intersept
                )

    def get_regression_line_values(self):
        return [i.value for i in self.regression_line_values]

    def calculate_regression_parameters(
        self,
        time_array,
        values_array,
    ):

        # Линейная регрессия
        (
            self.regression_line_slope,
            self.regression_line_intercept,
            self.r_value,
            self.p_value,
            std_err,
        ) = stats.linregress(time_array, values_array)

        self.calculate_regression_values(time_array)

    def calculate_confidence_interval(
        self, time_array, values_array, number_of_intervals, confidence_level
    ):
        if type(self.regression_line_values) == List[CalculatedParameter]:
            # Доверительный интервал линейной регрессии
            # Дисперсия независимой переменной (времени)
            variance_of_midpoints = np.var(time_array)
            # Квадраты ошибок (разница между предсказанными и фактическими значениями)
            squared_errors = (self.get_regression_line_values() - values_array) ** 2
            # Остаточная дисперсия (оценка дисперсии ошибок)
            residual_variance = sum(squared_errors) / (number_of_intervals - 2)
            # Дисперсия предсказанных значений для каждой точки
            prediction_variance = residual_variance * (
                1
                + 1 / number_of_intervals
                + (time_array - np.mean(time_array)) ** 2 / variance_of_midpoints
            )
            # Стандартная ошибка предсказания
            prediction_std_error = np.sqrt(prediction_variance)
            # Критерий t-распределения
            t_value = stats.t.ppf(
                (1 + confidence_level) / 2, df=number_of_intervals - 2
            )
            # Границы доверительного интервала
            for i in self.regression_line_values:
                i.set_lower(i.value - t_value * prediction_std_error)
                i.set_upper(i.value + t_value * prediction_std_error)

            # гипотеза об отсутствии тренда
            mean_predictor_value = sum(time_array) / len(time_array)
            squared_deviations_from_mean = (time_array - mean_predictor_value) ** 2

            # Sa = (s2_T_FR * [i**2 for i in failure_rates] / (2 * sum(d_i2))) ** (1/2)
            slope_standard_error = np.sqrt(
                residual_variance / sum(squared_deviations_from_mean)
            )
            relative_slope_error = slope_standard_error / abs(
                self.get_regression_line_values()
            )
            self.is_trend_non_significant = relative_slope_error > t_value

    def calculate_regression_line(
        self, time_array, values_array, number_of_intervals, confidence_level
    ):
        self.calculate_regression_line(
            time_array,
            values_array,
        )
        self.calculate_confidence_interval(
            time_array, values_array, number_of_intervals, confidence_level
        )
