import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os
from output_statistic_analyzis_to_csv import output_statistic_analyzis_to_csv
from math import floor

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
    colored = False
):
    try:
        # if len(data) < 50:
        #     print("Предупреждение: рекомендуется не менее 50 значений для точного анализа")
        # if len(data) == 0:
        #     return None
        # Расчёт средней интенсивности отказов
        total_failures = len(data)
        if max(data) > (365 * 10):
            ten_years_passed = True
        else:
            ten_years_passed = False
        if total_failures < 10:
            avg_failure_rate = (2 * total_failures + 1) / (2 * number_of_items * max(data))
        else:
            avg_failure_rate = total_failures / (number_of_items * max(data))
        if ten_years_passed:
            if total_failures < 10:
                avg_failure_rate_2 = (2 * total_failures + 1)  / (2 * number_of_items * 365 * 10)
            else:
                avg_failure_rate_2 = total_failures / (number_of_items * 365 * 10)
            
        df = total_failures - 2
    
        # Квантили распределения хи-квадрат
        chi2_lower = stats.chi2.ppf((1 - confidence_level) / 2, 2 * total_failures)
        chi2_upper = stats.chi2.ppf((1 + confidence_level) / 2, 2 * total_failures)
        # Доверительные границы
        avg_failure_rate_chi2_сonfidence_interval_lower_border = (avg_failure_rate * chi2_lower) / (2 * total_failures)
        avg_failure_rate_chi2_сonfidence_interval_upper_border = (avg_failure_rate * chi2_upper) / (2 * total_failures)
        if ten_years_passed:
            avg_failure_rate_2_chi2_сonfidence_interval_lower_border = (avg_failure_rate_2 * chi2_lower) / (2 * total_failures)
            avg_failure_rate_2_chi2_сonfidence_interval_upper_border = (avg_failure_rate_2 * chi2_upper) / (2 * total_failures)
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
        failure_rates2 = counts_in_intervals / (365 * 10 * number_of_items)

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
        
        # гипотеза об отсутствии тренда
        avg_midpoints_of_intervals = sum(midpoints_of_intervals)/len(midpoints_of_intervals)
        d_i2 = (midpoints_of_intervals - avg_midpoints_of_intervals)**2
        
        # Sa = (s2_T_FR * [i**2 for i in failure_rates] / (2 * sum(d_i2))) ** (1/2)
        Sb = (s2_T_FR / sum(d_i2)) ** (1/2)
        tsb = Sb / abs(regression_line_slope)
        gipoteza = tsb > t_value
        # Доверительный интервал по хи-квадрат
        df = number_of_intervals - 2
    
        # Квантили распределения хи-квадрат
        chi2_lower = stats.chi2.ppf((1 - confidence_level) / 2, df)
        chi2_upper = stats.chi2.ppf((1 + confidence_level) / 2, df)
        
        # Доверительные границы
        chi2_сonfidence_interval_lower_border = (failure_rates * chi2_lower) / (2 * total_failures)
        chi2_сonfidence_interval_upper_border = (failure_rates * chi2_upper) / (2 * total_failures)
    
        # Построение графика
        plt.figure(figsize=(graph_width, graph_width / 1.5))
        if colored:
            colors = {
                "group_intensivity": "#829fe3",
                "average_intensivity":"r",
                "decade_intensivity":"b",
                "standart_intensivity":"tab:orange", 
                "approximation":"g",
                "average_intensivity_interval":'#ff5050',
                "decade_intensivity_interval": "#bb99ff", 
                "approximation_interval" : "m"
            }
        else:
            colors = {
                "group_intensivity": "#999999",
                "average_intensivity":"#000000",
                "decade_intensivity":"#000000",
                "standart_intensivity":"000000", 
                "approximation":"#555555",
                "average_intensivity_interval":'#afafaf',
                "decade_intensivity_interval": "#aaaaaa", 
                "approximation_interval" : "#777777"
            }
        # Гистограмма интенсивности отказов
        plt.bar(
            midpoints_of_intervals,
            failure_rates,
            width=interval_width * 0.8,
            align="center",
            color = colors["group_intensivity"],
            alpha=0.7,
            hatch = "|||",
            label="Групповая интенсивность ",
        )
        # # Гистограмма интенсивности отказов2
        # plt.bar(
        #     midpoints_of_intervals,
        #     failure_rates2,
        #     width=interval_width * 0.8,
        #     align="center",
        #     alpha=0.7,
        #     color = "#bbaaff",
        #     label="Интенсивность отказов2",
        # )

        # Средняя интенсивность
        plt.axhline(
            y=avg_failure_rate,
            color=colors["average_intensivity"],
            linestyle="--",
            label=f"Средняя интенсивность"#: {avg_failure_rate:.2e},\nкол-во отказов: {total_failures}, кол-во оборудования: {number_of_items}",
        )
        # Средняя интенсивность2
        if ten_years_passed:
            plt.axhline(
                y=avg_failure_rate_2,
                color=colors["decade_intensivity"],
                linestyle="-.",
                label=f"Десятилетняя интенсивность"#: {avg_failure_rate:.2e},\nкол-во отказов: {total_failures}, кол-во оборудования: {number_of_items}",
            )
        if standart_intensivity:
            # Интенсивность по ВАБ
            plt.axhline(
                y=standart_intensivity,
                color=colors["standart_intensivity"],
                linestyle="-",
                label=f"Интенсивность по ВАБ"#: {standart_intensivity:.2e}",
            )

        # Линейная аппроксимация
        plt.plot(
            midpoints_of_intervals,
            regression_line,
            color = colors["approximation"],
            linestyle = ":",
            linewidth=2,
            label=f"Линейная аппроксимация"#: y = {regression_line_slope:.2e}x + {regression_line_intercept:.2e}\nP-уровень: {p_value:.2f}; R-уровень: {r_value:.2f}; P={confidence_level}",
        )
        plt.axhspan(
                avg_failure_rate_chi2_сonfidence_interval_lower_border,  # нижняя граница
                avg_failure_rate_chi2_сonfidence_interval_upper_border,  # верхняя граница
                alpha=0.3,         # прозрачность
                color=colors["average_intensivity_interval"],
                # hatch = "///",
                label = "Доверительный интервал \nсредней интенсивности"
                )
        if ten_years_passed:
            plt.axhspan(
                    avg_failure_rate_2_chi2_сonfidence_interval_lower_border,  # нижняя граница
                    avg_failure_rate_2_chi2_сonfidence_interval_upper_border,  # верхняя граница
                    alpha=0.3,         # прозрачность
                    # hatch = "\\\\\\",
                    color=colors["decade_intensivity_interval"],
                    label = "Доверительный интервал \nдесятилетней интенсивности"
                    )
        # plt.errorbar(
        #     midpoints_of_intervals,
        #     regression_line,
        #     yerr = (сonfidence_interval_upper_border - regression_line),
        #     capsize=3,    # размер "шапочки"
        #     capthick=1,   # толщина "шапочки"
        #     fmt='o',      # маркер
        #     ecolor='red', # цвет планок
        #     markersize=4,
        #     # "g--",
        #     linewidth=2,
        #     # label=f"Аппроксимация: y = {regression_line_slope:.2e}x + {regression_line_intercept:.2e}\nP-уровень: {p_value:.2f}; R-уровень: {r_value:.2f}; P={confidence_level}",
        # )

        # Верхняя доверительная граница аппроксимации
        plt.plot(
            midpoints_of_intervals,
            сonfidence_interval_upper_border,
            color = colors["approximation_interval"],
            linestyle = ":",
            linewidth=0.75,
            label=f"Верхняя доверительная\n граница аппроксимации"#(P={confidence_level})",
        )
        
        
        # # Верхняя доверительная граница интенсивности отказов
        # plt.plot(
        #     midpoints_of_intervals,
        #     chi2_сonfidence_interval_upper_border,
        #     "-",
        #     color = "#ff00aa",
        #     linewidth=1.5,
        #     label=f"Верхняя доверительная граница интенсивности отказов(P={confidence_level})",
        # )
        # # Верхняя доверительная граница
        # plt.plot(
        #     midpoints_of_intervals,
        #     chi2_сonfidence_interval_lower_border,
        #     "-",
        #     color = "#ee00aa",
        #     linewidth=1.5,
        #     label=f"Нижняя доверительная граница интенсивности отказов(P={confidence_level})",
        # )
        plt.ylim(bottom = 0)
        ax = plt.gca()
        yticks = ax.get_yticks()
        degree = floor(np.log10(np.max(np.abs(yticks[-1]))))
        new_yticks = [tick * (10 ** -degree) for tick in yticks]
        ax.set_yticklabels([f"{tick:.2f}" for tick in new_yticks])
        # Настройка графика
        plt.xlabel("Наработка (сутки)")
        plt.ylabel("Интенсивность отказов, $10^{" + str(degree) + "}$/сут")
        plt.title(f"{os.path.splitext(os.path.basename(output_file_path))[0]}")
        # plt.title(f"Анализ интенсивности отказов\n{os.path.splitext(os.path.basename(output_file_path))[0]}")
        # plt.xlim(left = 0)
        plt.grid(True, alpha=0.3)
        # plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
        plt.subplots_adjust(bottom=0.2)
        # Сохранение и отображение
        # plt.tight_layout()
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        # dir_name = os.path.dirname(output_file_path)
        # file_name = os.path.basename(output_file_path)
        # output_file_path = os.path.join(dir_name, f"{len(data)}_{file_name}")
        
        directory_path = os.path.dirname(output_file_path)
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path, exist_ok=True)
        name_without_ext = os.path.splitext(output_file_path)[0]
        output_file_path_without_label = f"{name_without_ext}_without_legend.jpg"
        plt.savefig(output_file_path_without_label, dpi=300, bbox_inches="tight")
        
        # легенда справа 
        plt.legend(loc='center left',          # расположение внутри bbox
          bbox_to_anchor=(1, 0.5),  # (x, y) относительно осей
          ncol=1,                       # колонок в легенде
          frameon=True,                 # рамка
          fancybox=True)                  # тень
        
        # легенда снизу 
        # plt.legend(loc='upper center',          # расположение внутри bbox
        #   bbox_to_anchor=(0.5, -0.5),  # (x, y) относительно осей
        #   ncol=2,                       # колонок в легенде
        #   frameon=True,                 # рамка
        #   fancybox=True,                # скругленные углы
        #   shadow=True)                  # тень
        

        
        plt.savefig(output_file_path, dpi=300, bbox_inches="tight")
        
        plt.savefig(os.path.join(os.path.dirname(os.path.dirname(output_file_path)), os.path.basename(output_file_path)), dpi=300, bbox_inches="tight")
        # print(f"Результат сохранён в файл: {output_file}")
        # plt.show()
        plt.close()

        #------------------------------------------------------------

        # # Построение графика c полной легендой
        # plt.figure(figsize=(graph_width, graph_width * 1.5))

        # # Гистограмма интенсивности отказов
        # plt.bar(
        #     midpoints_of_intervals,
        #     failure_rates,
        #     width=interval_width * 0.8,
        #     align="center",
        #     alpha=0.7,
        #     label="Интенсивность отказов",
        # )

        # # Средняя интенсивность
        # plt.axhline(
        #     y=avg_failure_rate,
        #     color="r",
        #     linestyle="-",
        #     label=f"Средняя интенсивность: {avg_failure_rate:e}",
        # )
        # if standart_intensivity:
        #     # Интенсивность по ВАБ
        #     plt.axhline(
        #         y=standart_intensivity,
        #         color="tab:orange",
        #         linestyle="-",
        #         label=f"Интенсивность по ВАБ: {standart_intensivity:e}",
        #     )
        #     plt.axhline(
        #         y=avg_failure_rate_chi2_сonfidence_interval_upper_border,
        #         color="tab:red",
        #         linestyle="-",
        #         label=f"верхняя доверительная граница: {avg_failure_rate_chi2_сonfidence_interval_upper_border:e}",
        #     )

        # # Линейная аппроксимация
        # plt.plot(
        #     midpoints_of_intervals,
        #     regression_line,
        #     "g--",
        #     linewidth=2,
        #     label=f"{gipoteza};Аппроксимация: y = {regression_line_slope:e}x + {regression_line_intercept:e}\nP-уровень: {p_value:.2f}; R-уровень: {r_value:.2f}; ",
        # )

        # # Верхняя доверительная граница аппроксимации
        # plt.plot(
        #     midpoints_of_intervals,
        #     сonfidence_interval_upper_border,
        #     "m-",
        #     linewidth=1.5,
        #     label=f"Верхняя доверительная граница аппроксимации(P={confidence_level})",
        # )
        # # Верхняя доверительная граница интенсивности отказов
        # plt.plot(
        #     midpoints_of_intervals,
        #     chi2_сonfidence_interval_upper_border,
        #     "-",
        #     color = "#ff00aa",
        #     linewidth=1.5,
        #     label=f"Верхняя доверительная граница интенсивности отказов(P={chi2_сonfidence_interval_upper_border})",
        # )
        # # Верхняя доверительная граница
        # plt.plot(
        #     midpoints_of_intervals,
        #     chi2_сonfidence_interval_lower_border,
        #     "-",
        #     color = "#ee00aa",
        #     linewidth=1.5,
        #     label=f"Нижняя доверительная граница интенсивности отказов(P={сonfidence_interval_lower_border})",
        # )

        # # Настройка графика
        # plt.xlabel("Наработка (сутки)")
        # plt.ylabel(f"Интенсивность отказов, 1/сут")
        # plt.title("Анализ интенсивности отказов")
        # # plt.legend()
        # plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        # plt.legend(ncol=2, loc='upper center' )# перемещение легенды графика
        # # plt.legend(bbox_to_anchor=(0.5, -0.2), loc='upper center' )# перемещение легенды графика
        # plt.grid(True, alpha=0.3)
        # plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

        # # Сохранение и отображение
        # plt.tight_layout()
        # # dir_name = os.path.dirname(output_file_path)
        # # file_name = os.path.basename(output_file_path)
        # # output_file_path = os.path.join(dir_name, f"{len(data)}_{file_name}")
        # name_without_ext = os.path.splitext(output_file_path)[0]
        # output_file_path_label = f"{name_without_ext}_label.jpg"
        # # plt.savefig(output_file_path_label, dpi=300, bbox_inches="tight")
        # # print(f"Результат сохранён в файл: {output_file}")
        # # plt.show()
        # plt.close()
        if not ten_years_passed:
            avg_failure_rate_2 = None
            avg_failure_rate_2_chi2_сonfidence_interval_lower_border = None
            avg_failure_rate_2_chi2_сonfidence_interval_upper_border = None
            
        statistic = (            
            data,
            number_of_items,
            total_failures,
            avg_failure_rate,
            avg_failure_rate_2,
            interval_width,
            intervals_borders,
            regression_line_slope,
            regression_line_intercept,
            failure_rates,
            counts_in_intervals,
            midpoints_of_intervals,
            сonfidence_interval_upper_border,
            сonfidence_interval_lower_border,
            chi2_сonfidence_interval_upper_border,
            chi2_сonfidence_interval_lower_border,
            avg_failure_rate_chi2_сonfidence_interval_lower_border,
            avg_failure_rate_chi2_сonfidence_interval_upper_border,
            avg_failure_rate_2_chi2_сonfidence_interval_lower_border,
            avg_failure_rate_2_chi2_сonfidence_interval_upper_border,
            p_value,
            r_value)
        output_statistic_analyzis_to_csv(
            output_file_path,
            data,
            number_of_items,
            total_failures,
            avg_failure_rate,
            avg_failure_rate_2,
            interval_width,
            intervals_borders,
            regression_line_slope,
            regression_line_intercept,
            failure_rates,
            counts_in_intervals,
            midpoints_of_intervals,
            сonfidence_interval_upper_border,
            сonfidence_interval_lower_border,
            chi2_сonfidence_interval_upper_border,
            chi2_сonfidence_interval_lower_border,
            avg_failure_rate_chi2_сonfidence_interval_lower_border,
            avg_failure_rate_chi2_сonfidence_interval_upper_border,
            avg_failure_rate_2_chi2_сonfidence_interval_lower_border,
            avg_failure_rate_2_chi2_сonfidence_interval_upper_border,
            p_value,
            r_value
        )

        return statistic
    except Exception as exception:
        print(output_file_path, exception)
