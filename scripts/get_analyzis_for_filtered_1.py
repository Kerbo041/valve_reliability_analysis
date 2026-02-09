import os
from model.valve import Valve
from model.defect import Defect
from calculate_defect_intensivity import get_analysis_result
from typing import Dict, List, Tuple


def get_analyzis_for_filtered_1(
    valve_list: Dict[str, Valve], NUMBER_OF_INTERVALS, NUMBER_OF_ITEMS, CONFIDENCE_LEVEL
):
    gatevalves_5_block_ngz = []
    gatevalves_6_7_block_ngz = []
    valves_shutoff_6_7_block_ngz = []

    valves_shutoff_5_block_oz = []
    valves_shutoff_6_block_oz = []
    gatevalves_5_block_oz = []
    gatevalves_6_7_block_oz = []

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
                        # дефекты типа НГЗ
                        if defect.defect_type.upper() == "Пропуск".upper():
                            if valve_list[valve_name].main_valve_type == "Задвижка":
                                if valve_list[valve_name].block_number == "5":
                                    gatevalves_5_block_ngz.append(value)
                                if valve_list[valve_name].block_number == "6-7":
                                    gatevalves_6_7_block_ngz.append(value)
                            if (valve_list[valve_name].block_number == "6-7") and (
                                valve_list[valve_name].valve_type == "Вентиль запорный"
                                or valve_list[valve_name].valve_type
                                == "Клапан запорный"
                                or valve_list[valve_name].valve_type
                                == "Клапан сильфонный"
                            ):
                                valves_shutoff_6_7_block_ngz.append(value)
                        # дефекты типа ОЗ
                        for defect_type in [
                            "Недозакрытие",
                            "Тугой ход",
                            "Клин",
                            "Выжат сальник",
                            "Обрыв",
                            "Отказ управления",
                            "Погнут шток",
                        ]:
                            if defect.defect_type.upper() == defect_type.upper():
                                if (
                                    valve_list[valve_name].valve_type
                                    == "Вентиль запорный"
                                    or valve_list[valve_name].valve_type
                                    == "Клапан запорный"
                                    or valve_list[valve_name].valve_type
                                    == "Клапан сильфонный"
                                ):
                                    if valve_list[valve_name].block_number == "5":
                                        valves_shutoff_5_block_oz.append(value)
                                    if (
                                        valve_list[valve_name].block_number == "6"
                                        or valve_list[valve_name].block_number == "7"
                                    ):
                                        valves_shutoff_6_block_oz.append(value)
                                elif (
                                    valve_list[valve_name].main_valve_type == "Задвижка"
                                ):
                                    if valve_list[valve_name].block_number == "5":
                                        gatevalves_5_block_oz.append(value)
                                    if (
                                        valve_list[valve_name].block_number == "6"
                                        or valve_list[valve_name].block_number == "7"
                                    ):
                                        gatevalves_6_7_block_oz.append(value)

                    except Exception as exception:
                        pass

    arrays = {
        "Задвижки, блок 5 НВОАЭС, отказ типа НГЗ": gatevalves_5_block_ngz,
        "Задвижки, блок 6-7 НВОАЭС, отказ типа НГЗ": gatevalves_6_7_block_ngz,
        "Вентили запорные, блок 5 НВОАЭС, отказы типа ОЗ объединённые": valves_shutoff_5_block_oz,
        "Вентили запорные, блок 6-7 НВОАЭС-2, отказы типа ОЗ объединённые": valves_shutoff_6_block_oz,
        "Задвижки, блок 5 НВОАЭС, отказы типа ОЗ объединённые": gatevalves_5_block_oz,
        "Задвижки, блок 6-7 НВОАЭС, отказы типа ОЗ объединённые": gatevalves_6_7_block_oz,
    }
    valve_type = None
    defect_type = None
    base_path = "files//result_filtered_1//"
    for filter_array_name in arrays:
        output_file_path = os.path.join(base_path, f"{filter_array_name}.png")
        directory_path = os.path.dirname(output_file_path)
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path, exist_ok=True)
        get_analysis_result(
            arrays[filter_array_name],
            valve_type,
            defect_type,
            output_file_path,
            NUMBER_OF_INTERVALS,
            NUMBER_OF_ITEMS,
            CONFIDENCE_LEVEL,
        )
