import os
from model.valve import Valve
from model.defect import Defect
from calculate_defect_intensivity import calculate_defect_intensivity
from typing import Dict, List, Tuple


def get_analyzis_for_filtered_2(
    valve_list: Dict[str, Valve],
    NUMBER_OF_INTERVALS,
    NUMBER_OF_ITEMS,
    CONFIDENCE_LEVEL,
    base_path="files//result_filtered//",
):

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
        if (
            valve_list[valve_name].commissioning_date is not None
            and valve_list[valve_name].main_valve_type is not None
        ):
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
                        if (
                            valve_list[valve_name].valve_type == "Вентиль запорный"
                            or valve_list[valve_name].valve_type == "Клапан запорный"
                            or valve_list[valve_name].valve_type == "Клапан сильфонный"
                        ):
                            filtered_arrays["Вентили запорные"][
                                valve_list[valve_name].get_block_number()
                            ][defect.defect_class].append(value)
                    except Exception as exception:
                        pass

    defect_type = None
    for valve_type in filtered_arrays:
        for block_number in filtered_arrays[valve_type]:
            for defect_class in filtered_arrays[valve_type][block_number]:
                file_name = (
                    f"{valve_type}, блок {block_number} НВАЭС, {defect_class}.png"
                )
                output_file_path = os.path.join(base_path, file_name)
                directory_path = os.path.dirname(output_file_path)
                if not os.path.isdir(directory_path):
                    os.makedirs(directory_path, exist_ok=True)
                calculate_defect_intensivity(
                    filtered_arrays[valve_type][block_number][defect_class],
                    valve_type,
                    defect_type,
                    output_file_path,
                    NUMBER_OF_INTERVALS,
                    NUMBER_OF_ITEMS,
                    CONFIDENCE_LEVEL,
                )
