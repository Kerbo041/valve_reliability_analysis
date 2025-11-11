import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
from output_statistic_analyzis_to_csv import output_statistic_analyzis_to_csv


def calculate_defect_intensivity(
    data,
    valve_type,
    defect_type,
    output_file_path,
    number_of_intervals,
    number_of_items,
    confidence_level=0.9,
    standart_intensivity=None,
    graph_width=5.9055,
):
    try:
        # if len(data) < 50:
        #     print("Предупреждение: рекомендуется не менее 50 значений для точного анализа")
        # if len(data) == 0:
        #     return None
        total_failures = len(data)

        # Расчёт средней интенсивности отказов
        avg_failure_rate = total_failures / (number_of_items * max(data))

        # Создание интервалов
        max_time = max(data)
        min_time = min(data)
        interval_width = (max_time - min_time) / number_of_intervals
        intervals_borders = np.linspace(min_time, max_time, number_of_intervals + 1)
        midpoints_of_intervals = (intervals_borders[:-1] + intervals_borders[1:]) / 2

        # Подсчёт отказов в интервалах
        counts_in_intervals, _ = np.histogram(data, bins=intervals_borders)

        # Расчёт интенсивности отказов для каждого интервала
        failure_rates = counts_in_intervals / (interval_width * number_of_items)

        # Линейная регрессия
        regression_line_slope, regression_line_intercept, r_value, p_value, std_err = (
            stats.linregress(midpoints_of_intervals, failure_rates)
        )
        regression_line = (
            regression_line_intercept + regression_line_slope * midpoints_of_intervals
        )

        # Доверительный интервал
        s2_T = np.var(midpoints_of_intervals)
        err_FR_2 = (regression_line - failure_rates) ** 2
        s2_T_FR = sum(err_FR_2) / (number_of_intervals - 2)
        s2_FR = s2_T_FR * (
            1
            + 1 / number_of_intervals
            + (midpoints_of_intervals - np.mean(midpoints_of_intervals)) ** 2 / s2_T
        )
        stderr_FR = np.sqrt(s2_FR)
        t_value = stats.t.ppf((1 + confidence_level) / 2, df=number_of_intervals - 2)
        сonfidence_interval_upper_border = regression_line + t_value * stderr_FR
        сonfidence_interval_lower_border = regression_line - t_value * stderr_FR

        # Построение графика
        plt.figure(figsize=(graph_width, graph_width / 1.5))

        # Гистограмма интенсивности отказов
        plt.bar(
            midpoints_of_intervals,
            failure_rates,
            width=interval_width * 0.8,
            align="center",
            alpha=0.7,
            label="Интенсивность отказов",
        )

        # Средняя интенсивность
        plt.axhline(
            y=avg_failure_rate,
            color="r",
            linestyle="-",
            label=f"Средняя интенсивность: {avg_failure_rate:e}",
        )
        if standart_intensivity:
            # Интенсивность по ВАБ
            plt.axhline(
                y=standart_intensivity,
                color="tab:orange",
                linestyle="-",
                label=f"Интенсивность по ВАБ: {standart_intensivity:e}",
            )

        # Линейная аппроксимация
        plt.plot(
            midpoints_of_intervals,
            regression_line,
            "g--",
            linewidth=2,
            label=f"Аппроксимация: y = {regression_line_slope:e}x + {regression_line_intercept:e}\nP-уровень: {p_value:.2f}",
        )

        # Верхняя доверительная граница
        plt.plot(
            midpoints_of_intervals,
            сonfidence_interval_upper_border,
            "m-",
            linewidth=1.5,
            label=f"Верхняя доверительная граница (P={confidence_level})",
        )

        # Настройка графика
        plt.xlabel("Наработка (сутки)")
        plt.ylabel("Интенсивность отказов, 1/сут")
        plt.title("Анализ интенсивности отказов")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

        # Сохранение и отображение
        plt.tight_layout()
        # dir_name = os.path.dirname(output_file_path)
        # file_name = os.path.basename(output_file_path)
        # output_file_path = os.path.join(dir_name, f"{len(data)}_{file_name}")
        plt.savefig(output_file_path, dpi=300, bbox_inches="tight")
        # print(f"Результат сохранён в файл: {output_file}")
        # plt.show()
        plt.close()
        x2_value = 0
        statistic = (            
            data,
            number_of_items,
            total_failures,
            avg_failure_rate,
            interval_width,
            intervals_borders,
            regression_line_slope,
            regression_line_intercept,
            failure_rates,
            counts_in_intervals,
            midpoints_of_intervals,
            сonfidence_interval_upper_border,
            сonfidence_interval_lower_border,
            p_value,
            r_value,
            x2_value)
        output_statistic_analyzis_to_csv(
            output_file_path,
            data,
            number_of_items,
            total_failures,
            avg_failure_rate,
            interval_width,
            intervals_borders,
            regression_line_slope,
            regression_line_intercept,
            failure_rates,
            counts_in_intervals,
            midpoints_of_intervals,
            сonfidence_interval_upper_border,
            сonfidence_interval_lower_border,
            p_value,
            r_value,
            x2_value
        )

        return statistic
    except Exception as exception:
        pass
