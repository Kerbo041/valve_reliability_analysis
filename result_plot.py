from model.analysis import Analysis
from matplotlib import pyplot as plt
import os
from math import floor
import numpy as np


def make_graph_for_analysis(
    analysis: Analysis,
    graph_width=5.9055,
    colored=False,
):
    # Построение графика
    plt.figure(figsize=(graph_width, graph_width / 1.5))
    # задание цветов
    if colored:
        colors = {
            "group_intensivity": "#829fe3",
            "average_intensivity": "r",
            "decade_intensivity": "b",
            "standart_intensivity": "tab:orange",
            "approximation": "g",
            "average_intensivity_interval": "#ff5050",
            "decade_intensivity_interval": "#bb99ff",
            "approximation_interval": "m",
        }
    else:
        colors = {
            "group_intensivity": "#999999",
            "average_intensivity": "#000000",
            "decade_intensivity": "#000000",
            "standart_intensivity": "000000",
            "approximation": "#555555",
            "average_intensivity_interval": "#afafaf",
            "decade_intensivity_interval": "#aaaaaa",
            "approximation_interval": "#777777",
        }

    # Гистограмма интенсивности отказов
    plt.bar(
        analysis.operating_time_intervals.get_values(),
        analysis.group_average_intensity.get_values(),
        width=analysis.interval_width * 0.8,
        align="center",
        color=colors["group_intensivity"],
        alpha=0.7,
        hatch="|||",
        label="Групповая интенсивность ",
    )

    # Средняя интенсивность
    plt.axhline(
        y=analysis.average_operating_failure_rate.get_value(),
        color=colors["average_intensivity"],
        linestyle="--",
        label=f"Средняя интенсивность",
    )
    plt.axhspan(
        analysis.average_operating_failure_rate.lower,
        analysis.average_operating_failure_rate.upper,
        alpha=0.3,
        color=colors["average_intensivity_interval"],
        label="Доверительный интервал \nсредней интенсивности",
    )
    # Средняя интенсивность2
    if analysis.average_observation_failure_rate:
        plt.axhline(
            y=analysis.average_observation_failure_rate.get_value(),
            color=colors["decade_intensivity"],
            linestyle="-.",
            label=f"Десятилетняя интенсивность",
        )
        plt.axhspan(
            analysis.average_observation_failure_rate.lower,
            analysis.average_observation_failure_rate.upper,
            alpha=0.3,  # прозрачность
            # hatch = "\\\\\\",
            color=colors["decade_intensivity_interval"],
            label="Доверительный интервал \nдесятилетней интенсивности",
        )
    if analysis.standart_intensivity:
        # Интенсивность по ВАБ
        plt.axhline(
            y=analysis.standart_intensivity,
            color=colors["standart_intensivity"],
            linestyle="-",
            label=f"Интенсивность по ВАБ",
        )

    # Линейная аппроксимация
    if analysis.linear_regression:
        plt.plot(
            analysis.operating_time_intervals.get_values(),
            analysis.linear_regression.regression_line_values.get_values(),
            color=colors["approximation"],
            linestyle=":",
            linewidth=2,
            label=f"Линейная аппроксимация",
        )
        # Верхняя доверительная граница аппроксимации
        plt.plot(
            analysis.operating_time_intervals.get_values(),
            [i.upper for i in analysis.linear_regression.regression_line_values],
            color=colors["approximation_interval"],
            linestyle=":",
            linewidth=0.75,
            label=f"Верхняя доверительная\n граница аппроксимации",
        )
        # Гамма аппроксимация (пока нет в анализе)
        # plt.plot(
        #     midpoints_of_intervals,
        #     gamma_intensities,
        #     # color = colors["approximation"],
        #     linestyle=":",
        #     linewidth=2,
        #     label=f"Гамма-аппроксимация k = {k}",  #: y = {regression_line_slope:.2e}x + {regression_line_intercept:.2e}\nP-уровень: {p_value:.2f}; R-уровень: {r_value:.2f}; P={confidence_level}",
        # )

    # настройка порядка значений на оси ординат
    plt.ylim(bottom=0)
    ax = plt.gca()
    yticks = ax.get_yticks()
    degree = floor(np.log10(np.max(np.abs(yticks[-1]))))
    new_yticks = [tick * (10**-degree) for tick in yticks]
    ax.set_yticklabels([f"{tick:.2f}" for tick in new_yticks])

    # Настройка графика
    plt.xlabel("Наработка (сутки)")
    plt.ylabel("Интенсивность отказов, $10^{" + str(degree) + "}$/сут")
    plt.title(analysis.name)

    plt.grid(True, alpha=0.3)
    plt.subplots_adjust(bottom=0.2)

    # Сохранение и отображение
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    directory_path = os.path.dirname(analysis.output_file_path)
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    name_without_ext = os.path.splitext(analysis.output_file_path)[0]
    output_file_path_without_label = f"{name_without_ext}_without_legend.jpg"
    plt.savefig(output_file_path_without_label, dpi=300, bbox_inches="tight")

    # легенда справа
    plt.legend(
        loc="center left",  # расположение внутри bbox
        bbox_to_anchor=(1, 0.5),  # (x, y) относительно осей
        ncol=1,
        frameon=True,
        fancybox=True,
    )

    # легенда снизу
    # plt.legend(loc='upper center',          # расположение внутри bbox
    #   bbox_to_anchor=(0.5, -0.5),  # (x, y) относительно осей
    #   ncol=2,                       # колонок в легенде
    #   frameon=True,                 # рамка
    #   fancybox=True,                # скругленные углы
    #   shadow=True)                  # тень

    plt.savefig(analysis.output_file_path, dpi=300, bbox_inches="tight")

    plt.savefig(
        os.path.join(
            os.path.dirname(os.path.dirname(analysis.output_file_path)),
            os.path.basename(analysis.output_file_path),
        ),
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()
