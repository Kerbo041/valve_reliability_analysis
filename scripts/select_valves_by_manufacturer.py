from model.valve import Valve
from typing import List, Dict, Tuple
import os
from main import create_file, append_to_file
file_result_for_valves_error = create_file("files\\output\\valves_error.txt")
file_valves_error_type = create_file("files\\data\\valves_error_type.csv")
file_result_for_valves_no_defect_type = create_file(
    "files\\output\\valves_no_defect_type.txt"
)
# --------------------------------------------------------------------------------------
# Выбор задвижек по производителю и по производителю (с определением конкретного)
# --------------------------------------------------------------------------------------

def select_valves_by_type(valve_list:Dict[str, Valve], output_manufacturer_folder_path, output_manufacturer_defined_folder_path):
    manufacturers_data = {}
    manufacturers_defined_data = {}
    manufacturers_valve_type_data = {}
    for valve_name in valve_list:
        if (
            valve_list[valve_name].commissioning_date is not None
            and valve_list[valve_name].main_valve_type is not None
        ):
            for defect in valve_list[valve_name].defect_list:
                if defect.defect_date is not None:
                    try:
                        value = (
                            defect.defect_date - valve_list[valve_name].commissioning_date
                        ).days
                        if valve_list[valve_name].manufacturer is not None:
                            if (
                                valve_list[valve_name].manufacturer
                                not in manufacturers_data
                            ):
                                manufacturers_data[valve_list[valve_name].manufacturer] = []
                            manufacturers_data[valve_list[valve_name].manufacturer].append(
                                value
                            )
                            append_to_file(
                                os.path.join(
                                    output_manufacturer_folder_path,
                                    valve_list[valve_name].manufacturer,
                                ),
                                value,
                            )
                        if valve_list[valve_name].manufacturer_defined is not None:
                            if (
                                valve_list[valve_name].manufacturer_defined
                                not in manufacturers_defined_data
                            ):
                                manufacturers_defined_data[
                                    valve_list[valve_name].manufacturer_defined
                                ] = []
                            if valve_list[valve_name].valve_type is not None:
                                if (
                                    valve_list[valve_name].manufacturer_defined
                                    not in manufacturers_valve_type_data
                                ):
                                    manufacturers_valve_type_data[
                                        valve_list[valve_name].manufacturer_defined
                                    ] = {}
                                if (
                                    valve_list[valve_name].valve_type
                                    not in manufacturers_valve_type_data
                                ):
                                    manufacturers_valve_type_data[
                                        valve_list[valve_name].manufacturer_defined
                                    ][valve_list[valve_name].valve_type] = []
                                manufacturers_valve_type_data[
                                    valve_list[valve_name].manufacturer_defined
                                ][valve_list[valve_name].valve_type].append(value)
                            manufacturers_defined_data[
                                valve_list[valve_name].manufacturer_defined
                            ].append(value)
                            append_to_file(
                                os.path.join(
                                    output_manufacturer_defined_folder_path,
                                    valve_list[valve_name].manufacturer_defined,
                                ),
                                value,
                            )
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
                    except Exception as exception:
                        pass
                        print(valve_list[valve_name], file=file_result_for_valves_error)
                        print(defect, file=file_result_for_valves_error)
                        print(
                            "error with defect type/time", file=file_result_for_valves_error
                        )
                else:
                    print(valve_list[valve_name], file=file_result_for_valves_error)
                    print("no defect time", file=file_result_for_valves_error)
        else:
            print(valve_list[valve_name], file=file_result_for_valves_error)
            print("no commissioning time", file=file_result_for_valves_error)
# --------------------------------------------------------------------------------------