from model.valve import Valve
from typing import List, Dict, Tuple
from valve_type_analyzer import get_type_from_element_name, filter_valves_by_name
import os
def create_file(path):
    directory_path = os.path.dirname(path)
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    return open(path, "w", encoding="utf-8")

# --------------------------------------------------------------------------------------
# Вывод данных о найденных единицах оборудования и результатах их обработки
# --------------------------------------------------------------------------------------

file_valves_with_description = open("files\\data\\valves_with_description.csv", "w", encoding="utf-8")
file_valves_with_type = open("files\\valves_with_type.csv", "w", encoding="utf-8")
file_valves_without_description = open("files\\data\\valves_without_description.csv", "w", encoding="utf-8")
file_valves_with_main_type = open("files\\data\\valves_with_main_type.csv", "w", encoding="utf-8")
file_not_valves = create_file("files\\data\\not_valves.csv")


def output_readed_valves(valve_list:Dict[str, Valve], types_blacklist):
    for valve_name in valve_list:
        # if check_valve_type(valve_list[valve_name]):
        #     print(valve_list[valve_name], file=file_valves_error_type)
        if valve_list[valve_name].get_descritpion() != "":
            print(valve_list[valve_name], file=file_valves_with_description)
        elif valve_list[valve_name].valve_type is not None:
            print(valve_list[valve_name], file=file_valves_with_type)
        elif valve_list[valve_name].main_valve_type is not None:
            print(valve_list[valve_name], file=file_valves_with_main_type)
        elif filter_valves_by_name(valve_list[valve_name], types_blacklist):
            print(valve_list[valve_name], file=file_valves_without_description)
        else:
            print(valve_list[valve_name], file=file_not_valves)
# --------------------------------------------------------------------------------------