from src.model.reader_DTO.valve import Valve
from typing import List, Dict, Tuple
import os


def create_file(path):
    directory_path = os.path.dirname(path)
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    return open(path, "w", encoding="utf-8")


# --------------------------------------------------------------------------------------
# Выбор задвижек по типу
# --------------------------------------------------------------------------------------
file_result_for_valves_error = create_file("files\\output\\valves_error.txt")
file_valves_error_type = create_file("files\\data\\valves_error_type.csv")
file_result_for_valves_no_defect_type = create_file(
    "files\\output\\valves_no_defect_type.txt"
)


def select_valves_by_type(
    valve_list: Dict[str, Valve],
    defect_types: Dict[str, List[str]],
    types_whitelist: Dict[str, Dict[str, List[str]]],
):

    files_array_output = {
        valve_type: {
            defect_type: create_file(f"files\\output\\{valve_type}\\{defect_type}.txt")
            for defect_type in defect_types
        }
        for valve_type in types_whitelist
    }
    defect_array_output = {
        valve_type: {defect_type: [] for defect_type in defect_types}
        for valve_type in types_whitelist
    }

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
                        if defect.defect_type == None:
                            print(
                                valve_list[valve_name],
                                file=file_result_for_valves_no_defect_type,
                            )
                            print(defect, file=file_result_for_valves_no_defect_type)
                            print(
                                defect.defect_description,
                                file=file_result_for_valves_no_defect_type,
                            )
                            print("", file=file_result_for_valves_no_defect_type)
                        for defect_type in defect_types:
                            if defect.defect_type.upper() == defect_type.upper():
                                print(
                                    value,
                                    file=files_array_output[
                                        valve_list[valve_name].main_valve_type
                                    ][defect_type],
                                )
                                defect_array_output[
                                    valve_list[valve_name].main_valve_type
                                ][defect_type].append(value)
                    except Exception as exception:
                        pass
                        print(valve_list[valve_name], file=file_result_for_valves_error)
                        print(defect, file=file_result_for_valves_error)
                        print(
                            "error with defect type/time",
                            file=file_result_for_valves_error,
                        )
                else:
                    print(valve_list[valve_name], file=file_result_for_valves_error)
                    print("no defect time", file=file_result_for_valves_error)
        else:
            print(valve_list[valve_name], file=file_result_for_valves_error)
            print("no commissioning time", file=file_result_for_valves_error)
    return defect_array_output


# --------------------------------------------------------------------------------------
