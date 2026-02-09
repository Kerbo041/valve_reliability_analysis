from matplotlib import pyplot as plt


def plot_results(
    analysis,
    graph_width=5.9055,
    colored=False,
):
    # Построение графика
    plt.figure(figsize=(graph_width, graph_width / 1.5))
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
        midpoints_of_intervals,
        failure_rates_for_each_group,
        width=interval_width * 0.8,
        align="center",
        color=colors["group_intensivity"],
        alpha=0.7,
        hatch="|||",
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
        y=average_operating_failure_rate,
        color=colors["average_intensivity"],
        linestyle="--",
        label=f"Средняя интенсивность",  #: {avg_failure_rate:.2e},\nкол-во отказов: {total_failures}, кол-во оборудования: {number_of_items}",
    )
    # Средняя интенсивность2
    if operating_time_exceeds_observation:
        plt.axhline(
            y=average_observation_failure_rate,
            color=colors["decade_intensivity"],
            linestyle="-.",
            label=f"Десятилетняя интенсивность",  #: {avg_failure_rate:.2e},\nкол-во отказов: {total_failures}, кол-во оборудования: {number_of_items}",
        )
    if standart_intensivity:
        # Интенсивность по ВАБ
        plt.axhline(
            y=standart_intensivity,
            color=colors["standart_intensivity"],
            linestyle="-",
            label=f"Интенсивность по ВАБ",  #: {standart_intensivity:.2e}",
        )

    # Линейная аппроксимация
    plt.plot(
        midpoints_of_intervals,
        regression_line,
        color=colors["approximation"],
        linestyle=":",
        linewidth=2,
        label=f"Линейная аппроксимация",  #: y = {regression_line_slope:.2e}x + {regression_line_intercept:.2e}\nP-уровень: {p_value:.2f}; R-уровень: {r_value:.2f}; P={confidence_level}",
    )
    # Гамма аппроксимация
    plt.plot(
        midpoints_of_intervals,
        gamma_intensities,
        # color = colors["approximation"],
        linestyle=":",
        linewidth=2,
        label=f"Гамма-аппроксимация k = {k}",  #: y = {regression_line_slope:.2e}x + {regression_line_intercept:.2e}\nP-уровень: {p_value:.2f}; R-уровень: {r_value:.2f}; P={confidence_level}",
    )
    plt.axhspan(
        avg_failure_rate_chi2_сonfidence_interval_lower_border,  # нижняя граница
        avg_failure_rate_chi2_сonfidence_interval_upper_border,  # верхняя граница
        alpha=0.3,  # прозрачность
        color=colors["average_intensivity_interval"],
        # hatch = "///",
        label="Доверительный интервал \nсредней интенсивности",
    )
    if operating_time_exceeds_observation:
        plt.axhspan(
            avg_failure_rate_2_chi2_сonfidence_interval_lower_border,  # нижняя граница
            avg_failure_rate_2_chi2_сonfidence_interval_upper_border,  # верхняя граница
            alpha=0.3,  # прозрачность
            # hatch = "\\\\\\",
            color=colors["decade_intensivity_interval"],
            label="Доверительный интервал \nдесятилетней интенсивности",
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
        color=colors["approximation_interval"],
        linestyle=":",
        linewidth=0.75,
        label=f"Верхняя доверительная\n граница аппроксимации",  # (P={confidence_level})",
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
    plt.ylim(bottom=0)
    ax = plt.gca()
    yticks = ax.get_yticks()
    degree = floor(np.log10(np.max(np.abs(yticks[-1]))))
    new_yticks = [tick * (10**-degree) for tick in yticks]
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
    plt.legend(
        loc="center left",  # расположение внутри bbox
        bbox_to_anchor=(1, 0.5),  # (x, y) относительно осей
        ncol=1,  # колонок в легенде
        frameon=True,  # рамка
        fancybox=True,
    )  # тень

    # легенда снизу
    # plt.legend(loc='upper center',          # расположение внутри bbox
    #   bbox_to_anchor=(0.5, -0.5),  # (x, y) относительно осей
    #   ncol=2,                       # колонок в легенде
    #   frameon=True,                 # рамка
    #   fancybox=True,                # скругленные углы
    #   shadow=True)                  # тень

    plt.savefig(output_file_path, dpi=300, bbox_inches="tight")

    plt.savefig(
        os.path.join(
            os.path.dirname(os.path.dirname(output_file_path)),
            os.path.basename(output_file_path),
        ),
        dpi=300,
        bbox_inches="tight",
    )
    # print(f"Результат сохранён в файл: {output_file}")
    # plt.show()
    plt.close()

    # ------------------------------------------------------------

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
