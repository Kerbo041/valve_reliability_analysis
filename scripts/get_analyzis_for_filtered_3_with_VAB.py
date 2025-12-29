import os
from model.valve import Valve
from model.defect import Defect
from calculate_defect_intensivity import calculate_defect_intensivity
from typing import Dict, List, Tuple


def get_analyzis_for_filtered_3(
    valve_list: Dict[str, Valve],
    NUMBER_OF_INTERVALS,
    NUMBER_OF_ITEMS,
    CONFIDENCE_LEVEL,
    vab,
    base_path="files//result_filtered_with_vab//",
):
    valves_filtered = {
        "Задвижки": {
            "3-4": [],
            "5": [],
            "6-7": [],
        },
        "Вентили запорные": {"3-4": [], "5": [], "6-7": []},
    }
    filtered_arrays = {
        "Задвижки": {
            "3-4": {
                "отказ типа НГЗ": [],
                "отказ типа НГВ": [],
                "отказы типа ОЗ объединённые": [],
            },
            "5": {
                "отказ типа НГЗ": [],
                "отказ типа НГВ": [],
                "отказы типа ОЗ объединённые": [],
            },
            "6-7": {
                "отказ типа НГЗ": [],
                "отказ типа НГВ": [],
                "отказы типа ОЗ объединённые": [],
            },
        },
        "Вентили запорные": {
            "3-4": {
                "отказ типа НГЗ": [],
                "отказ типа НГВ": [],
                "отказы типа ОЗ объединённые": [],
            },
            "5": {
                "отказ типа НГЗ": [],
                "отказ типа НГВ": [],
                "отказы типа ОЗ объединённые": [],
            },
            "6-7": {
                "отказ типа НГЗ": [],
                "отказ типа НГВ": [],
                "отказы типа ОЗ объединённые": [],
            },
        },
    }

    # "Задвижки, блок 5 НВОАЭС, отказ типа НГЗ": [],
    # "Задвижки, блок 6-7 НВОАЭС, отказ типа НГЗ": gatevalves_6_7_block_ngz,
    # "Вентили запорные, блок 5 НВОАЭС, отказы типа ОЗ объединённые": valves_shutoff_5_block_oz,
    # "Вентили запорные, блок 6-7 НВОАЭС-2, отказы типа ОЗ объединённые": valves_shutoff_6_block_oz,
    # "Задвижки, блок 5 НВОАЭС, отказы типа ОЗ объединённые": gatevalves_5_block_oz,
    # "Задвижки, блок 6-7 НВОАЭС, отказы типа ОЗ объединённые": gatevalves_6_7_block_oz,

    for valve_name in valve_list:
        try:
            if (
                valve_list[valve_name].commissioning_date is not None
                and valve_list[valve_name].main_valve_type is not None
            ):
                if valve_list[valve_name].main_valve_type == "Задвижка":

                    valves_filtered["Задвижки"][
                        valve_list[valve_name].get_block_number()
                    ].append(valve_list[valve_name])
                if (
                    valve_list[valve_name].valve_type == "Вентиль запорный"
                    or valve_list[valve_name].valve_type == "Клапан запорный"
                    or valve_list[valve_name].valve_type == "Клапан сильфонный"
                ):

                    valves_filtered["Вентили запорные"][
                        valve_list[valve_name].get_block_number()
                    ].append(valve_list[valve_name])
                for defect in valve_list[valve_name].defect_list:
                    if defect.defect_date is not None:
                        try:
                            value = (
                                defect.defect_date
                                - valve_list[valve_name].commissioning_date
                            ).days

                            if valve_list[valve_name].main_valve_type == "Задвижка":
                                filtered_arrays["Задвижки"][
                                    valve_list[valve_name].get_block_number()
                                ][defect.defect_class].append(value)
                                # valves_filtered["Задвижки"][
                                #     valve_list[valve_name].get_block_number()
                                # ].append(valve_list[valve_name])
                            if (
                                valve_list[valve_name].valve_type == "Вентиль запорный"
                                or valve_list[valve_name].valve_type == "Клапан запорный"
                                or valve_list[valve_name].valve_type == "Клапан сильфонный"
                            ):
                                filtered_arrays["Вентили запорные"][
                                    valve_list[valve_name].get_block_number()
                                ][defect.defect_class].append(value)
                                # valves_filtered["Вентили запорные"][
                                #     valve_list[valve_name].get_block_number()
                                # ].append(valve_list[valve_name])
                        except Exception as exception:
                            pass
        except Exception as exception:
            print(exception)

    numbers_file_path = os.path.join(base_path, "result_numbers.csv")
    directory_path = os.path.dirname(numbers_file_path)
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    numbers_file = open(numbers_file_path, "w")
    print(
        f"тип;средняя интенсивность;кол-во единиц обороудования;кол-во отказов;коэффициент аппроксимации k;коэффициент аппроксимации x;p_value;r_value",
        file=numbers_file,
    )
    defect_type = None
    for valve_type in filtered_arrays:
        for block_number in filtered_arrays[valve_type]:
            for defect_class in filtered_arrays[valve_type][block_number]:
                file_name = (
                    f"{valve_type}, блок {block_number} НВАЭС, {defect_class}.jpg"
                )

                output_file_path = os.path.join(
                    base_path, os.path.splitext(file_name)[0]
                )
                output_file_path = os.path.join(output_file_path, file_name)
                # directory_path = os.path.dirname(output_file_path)
                # if not os.path.isdir(directory_path):
                #     os.makedirs(directory_path, exist_ok=True)
                result = calculate_defect_intensivity(
                    filtered_arrays[valve_type][block_number][defect_class],
                    valve_type,
                    defect_type,
                    output_file_path,
                    NUMBER_OF_INTERVALS,
                    len(valves_filtered[valve_type][block_number]),
                    CONFIDENCE_LEVEL,
                    vab[valve_type][block_number],
                )
                if result is not None:
                    (
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
                        chi2_сonfidence_interval_upper_border,
                        chi2_сonfidence_interval_lower_border,
                        avg_failure_rate_chi2_сonfidence_interval_lower_border,
                        avg_failure_rate_chi2_сonfidence_interval_upper_border,
                        p_value,
                        r_value,
                    ) = result
                    print(
                        f"{file_name};{avg_failure_rate};{number_of_items};{total_failures};{regression_line_slope};{regression_line_intercept};{p_value};{r_value}",
                        file=numbers_file,
                    )
