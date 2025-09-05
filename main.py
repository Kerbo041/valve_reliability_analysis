from defect_list_xslx_file_reader import get_defect_data_from_sheet
from torex_xlsb_file_reader import get_torex_data_from_sheet
from valve_type_search_in_torex import valve_type_search_in_torex
from valve_type_analyzer import get_type_from_element_name, filter_valves_by_name
from defect_type_analyzer import get_defect_type, get_defect_class
from calculate_defect_intensivity import calculate_defect_intensivity
from model.valve import Valve, Defect
from model.torex_record import TorexRecord
from json import load
from typing import Dict, List, Tuple
import openpyxl
import os
from scripts.get_analyzis_for_filtered_1 import get_analyzis_for_filtered_1
from scripts.get_analyzis_for_filtered_2 import get_analyzis_for_filtered_2

# ===== КОНФИГУРАЦИЯ =====
excel_file_path = (
    "files\\данные\\Карта данных 2015-2025.xlsx"  # Укажите путь к вашему файлу
)
torex_file_path = (
    "files\\данные\\Регистр ТОРЭКС_прореженный.xlsx"  # Укажите путь к вашему файлу
)
types_blacklist_path = "files\\settings\\names_blacklist.txt"
types_whitelist_path = "files\\settings\\names_whitelist.json"
defect_types_path = "files\\settings\\defect_list.json"
defect_classes_path = "files\\settings\\defect_classes.json"
manufacturers_path = "files\\settings\\manufacturers.json"
column_names_path = "column_names.json"
column_names_torex_path = "column_names_torex.json"
result_folder_path = "files\\result"
result_manufacturer_folder_path = "files\\result_manufacturer"
output_manufacturer_folder_path = "files\\output_manufacturer"
result_manufacturer_defined_folder_path = "files\\result_manufacturer_defined"
result_manufacturer_valve_type_folder_path = "files\\result_manufacturer_valve_type"
output_manufacturer_defined_folder_path = "files\\output_manufacturer_defined"
NUMBER_OF_INTERVALS = 10  # Количество интервалов разбиения
NUMBER_OF_ITEMS = 2181  # Общее количество наблюдаемых изделий
CONFIDENCE_LEVEL = 0.9  # Уровень доверия (P=0.9)
# =========================


def check_valve_type(valve: Valve):
    result = False
    if valve.valve_type is not None and valve.main_valve_type is not None:
        if valve.valve_type.upper().find(valve.main_valve_type.upper()) == -1 or (
            valve.get_descritpion() != ""
            and valve.get_descritpion().find(valve.main_valve_type.upper()) == -1
        ):
            result = True
    return result


def get_manufacturer_from_valve(valve: Valve, whitelist: Dict[str, str]):
    result = False
    for manufacturer in whitelist:
        for manufacturer_name_variant in whitelist[manufacturer]:
            if valve.manufacturer.upper().find(manufacturer_name_variant.upper()) != -1:
                result = True
                valve.manufacturer_defined = manufacturer
                return result
    return result


def create_file(path):
    directory_path = os.path.dirname(path)
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    return open(path, "w", encoding="utf-8")


def append_to_file(path, new_str):
    directory_path = os.path.dirname(path)
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path, exist_ok=True)
    with open(path, "a", encoding="utf-8") as file_to_append:
        print(new_str, file=file_to_append)


types_blacklist: List[str] = []

with open(types_blacklist_path, encoding="utf-8") as types_blacklist_file:
    for line in types_blacklist_file.readlines():
        types_blacklist.append(line.strip())
with open(types_whitelist_path, encoding="utf-8") as whitelist_file:
    types_whitelist = load(whitelist_file)
with open(defect_types_path, encoding="utf-8") as defect_types_file:
    defect_types = load(defect_types_file)
with open(column_names_path, encoding="utf-8") as column_names_file:
    column_names = load(column_names_file)
with open(column_names_torex_path, encoding="utf-8") as column_names_file:
    column_names_torex = load(column_names_file)
with open(manufacturers_path, encoding="utf-8") as manufacturers_file:
    manufacturers_list = load(manufacturers_file)
with open(defect_classes_path, encoding="utf-8") as defect_classes_file:
    defect_classes = load(defect_classes_file)

workbook = openpyxl.load_workbook(excel_file_path)
sheet_names = workbook.sheetnames
defect_list_file_data: List[List[Valve]] = []
for sheet_name in sheet_names:
    sheet = workbook[sheet_name]
    defect_list_file_data.append(get_defect_data_from_sheet(sheet, column_names))

valve_list = {
    f"{valve.get_block_number()}_{valve.get_valve_name_upper()}": valve
    for valve in defect_list_file_data[0]
}

workbook = openpyxl.load_workbook(torex_file_path)
sheet_names = workbook.sheetnames
torex_file_data: List[List[TorexRecord]] = []
for sheet_name in sheet_names:
    sheet = workbook[sheet_name]
    torex_file_data.append(get_torex_data_from_sheet(sheet, column_names_torex))

torex_list = {
    f"{torex_record.get_block_number()}_{torex_record.get_valve_name_operational_upper()}": torex_record
    for torex_record in torex_file_data[0]
}
torex_errors_file = open("files//torex_errors.csv", "w", encoding="utf-8")
for record in torex_list:
    if torex_list[record].valve_name_plant != torex_list[record].valve_name_operational:
        print(torex_list[record], file = torex_errors_file)

valve_type_search_in_torex(valve_list, torex_list)


file_result_for_valves_error = create_file("files\\output\\valves_error.txt")
file_result_for_valves_no_defect_type = create_file(
    "files\\output\\valves_no_defect_type.txt"
)
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
    get_type_from_element_name(valve_list[valve_name], types_whitelist)
    get_manufacturer_from_valve(valve_list[valve_name], manufacturers_list)
    get_defect_type(valve_list[valve_name], defect_types)
    get_defect_class(valve_list[valve_name], defect_classes)

get_analyzis_for_filtered_1(
    valve_list, NUMBER_OF_INTERVALS, NUMBER_OF_ITEMS, CONFIDENCE_LEVEL
)
get_analyzis_for_filtered_2(
    valve_list, NUMBER_OF_INTERVALS, NUMBER_OF_ITEMS, CONFIDENCE_LEVEL
)

# file_valves_all = create_file("files\\data\\all.csv")

# for valve_name in valve_list:
#     print(valve_list[valve_name], file=file_valves_all)

# --------------------------------------------------------------------------------------
# Вывод данных о найденных единицах оборудования и результатах их обработки
# --------------------------------------------------------------------------------------
#
# file_valves_with_description = open("files\\data\\valves_with_description.csv", "w", encoding="utf-8")
# file_valves_with_type = open("files\\valves_with_type.csv", "w", encoding="utf-8")
# file_valves_without_description = open("files\\data\\valves_without_description.csv", "w", encoding="utf-8")
# file_valves_with_main_type = open("files\\data\\valves_with_main_type.csv", "w", encoding="utf-8")
# file_not_valves = create_file("files\\data\\not_valves.csv")
# file_valves_error_type = create_file("files\\data\\valves_error_type.csv")
#
# for valve_name in valve_list:
#     # if check_valve_type(valve_list[valve_name]):
#     #     print(valve_list[valve_name], file=file_valves_error_type)
#     if valve_list[valve_name].get_descritpion() != "":
#         print(valve_list[valve_name], file=file_valves_with_description)
#     elif valve_list[valve_name].valve_type is not None:
#         print(valve_list[valve_name], file=file_valves_with_type)
#     elif valve_list[valve_name].main_valve_type is not None:
#         print(valve_list[valve_name], file=file_valves_with_main_type)
#     elif filter_valves_by_name(valve_list[valve_name], types_blacklist):
#         print(valve_list[valve_name], file=file_valves_without_description)
#     else:
#         print(valve_list[valve_name], file=file_not_valves)
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# Выбор задвижек по типу, по производителю и по производителю (с определением конкретного)
# --------------------------------------------------------------------------------------
# manufacturers_data = {}
# manufacturers_defined_data = {}
# manufacturers_valve_type_data = {}
# for valve_name in valve_list:
#     if (
#         valve_list[valve_name].commissioning_date is not None
#         and valve_list[valve_name].main_valve_type is not None
#     ):
#         for defect in valve_list[valve_name].defect_list:
#             if defect.defect_date is not None:
#                 try:
#                     value = (
#                         defect.defect_date - valve_list[valve_name].commissioning_date
#                     ).days
#                     if valve_list[valve_name].manufacturer is not None:
#                         if (
#                             valve_list[valve_name].manufacturer
#                             not in manufacturers_data
#                         ):
#                             manufacturers_data[valve_list[valve_name].manufacturer] = []
#                         manufacturers_data[valve_list[valve_name].manufacturer].append(
#                             value
#                         )
#                         append_to_file(
#                             os.path.join(
#                                 output_manufacturer_folder_path,
#                                 valve_list[valve_name].manufacturer,
#                             ),
#                             value,
#                         )
#                     if valve_list[valve_name].manufacturer_defined is not None:
#                         if (
#                             valve_list[valve_name].manufacturer_defined
#                             not in manufacturers_defined_data
#                         ):
#                             manufacturers_defined_data[
#                                 valve_list[valve_name].manufacturer_defined
#                             ] = []
#                         if valve_list[valve_name].valve_type is not None:
#                             if (
#                                 valve_list[valve_name].manufacturer_defined
#                                 not in manufacturers_valve_type_data
#                             ):
#                                 manufacturers_valve_type_data[
#                                     valve_list[valve_name].manufacturer_defined
#                                 ] = {}
#                             if (
#                                 valve_list[valve_name].valve_type
#                                 not in manufacturers_valve_type_data
#                             ):
#                                 manufacturers_valve_type_data[
#                                     valve_list[valve_name].manufacturer_defined
#                                 ][valve_list[valve_name].valve_type] = []
#                             manufacturers_valve_type_data[
#                                 valve_list[valve_name].manufacturer_defined
#                             ][valve_list[valve_name].valve_type].append(value)
#                         manufacturers_defined_data[
#                             valve_list[valve_name].manufacturer_defined
#                         ].append(value)
#                         append_to_file(
#                             os.path.join(
#                                 output_manufacturer_defined_folder_path,
#                                 valve_list[valve_name].manufacturer_defined,
#                             ),
#                             value,
#                         )
#                     if defect.defect_type == None:
#                         print(
#                             valve_list[valve_name],
#                             file=file_result_for_valves_no_defect_type,
#                         )
#                         print(defect, file=file_result_for_valves_no_defect_type)
#                         print(
#                             defect.defect_description,
#                             file=file_result_for_valves_no_defect_type,
#                         )
#                         print("", file=file_result_for_valves_no_defect_type)
#                     for defect_type in defect_types:
#                         if defect.defect_type.upper() == defect_type.upper():
#                             print(
#                                 value,
#                                 file=files_array_output[
#                                     valve_list[valve_name].main_valve_type
#                                 ][defect_type],
#                             )
#                             defect_array_output[valve_list[valve_name].main_valve_type][
#                                 defect_type
#                             ].append(value)
#                 except Exception as exception:
#                     pass
#                     print(valve_list[valve_name], file=file_result_for_valves_error)
#                     print(defect, file=file_result_for_valves_error)
#                     print(
#                         "error with defect type/time", file=file_result_for_valves_error
#                     )
#             else:
#                 print(valve_list[valve_name], file=file_result_for_valves_error)
#                 print("no defect time", file=file_result_for_valves_error)
#     else:
#         print(valve_list[valve_name], file=file_result_for_valves_error)
#         print("no commissioning time", file=file_result_for_valves_error)
# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# Выполнение статистического анализа для разных типов арматур и дефектов
# --------------------------------------------------------------------------------------
# for valve_type in defect_array_output:
#     for defect_type in defect_array_output[valve_type]:
#         output_file_path = os.path.join(result_folder_path, valve_type)
#         if not os.path.isdir(output_file_path):
#             os.makedirs(output_file_path, exist_ok=True)
#         output_file_path = os.path.join(
#             output_file_path, f"{valve_type}_{defect_type}_analysis.png"
#         )
#         calculate_defect_intensivity(
#             defect_array_output[valve_type][defect_type],
#             valve_type,
#             defect_type,
#             output_file_path,
#             NUMBER_OF_INTERVALS,
#             NUMBER_OF_ITEMS,
#             CONFIDENCE_LEVEL,
#         )
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Выполнение статистического анализа для разных производителей
# --------------------------------------------------------------------------------------
# for manufacturer in manufacturers_data:
#     result_file_path = result_manufacturer_folder_path
#     if not os.path.isdir(result_file_path):
#         os.makedirs(result_file_path, exist_ok=True)
#     result_file_path = os.path.join(
#         result_file_path, f"{manufacturer}_analysis.png"
#     )
#     valve_type = None
#     defect_type = None
#     calculate_defect_intensivity(
#         manufacturers_data[manufacturer],
#         valve_type,
#         defect_type,
#         result_file_path,
#         NUMBER_OF_INTERVALS,
#         NUMBER_OF_ITEMS,
#         CONFIDENCE_LEVEL,
#     )
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Выполнение статистического анализа для разных производителей (распознанных из сырой таблицы)
# --------------------------------------------------------------------------------------
# for manufacturer in manufacturers_defined_data:
#     result_file_path = result_manufacturer_defined_folder_path
#     if not os.path.isdir(result_file_path):
#         os.makedirs(result_file_path, exist_ok=True)
#     result_file_path = os.path.join(
#         result_file_path, f"{manufacturer}_analysis.png"
#     )
#     calculate_defect_intensivity(
#         manufacturers_defined_data[manufacturer],
#         valve_type,
#         defect_type,
#         result_file_path,
#         NUMBER_OF_INTERVALS,
#         NUMBER_OF_ITEMS,
#         CONFIDENCE_LEVEL,
#     )
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Выполнение статистического анализа для разных производителей (распознанных из сырой таблицы) по типам арматуры
# --------------------------------------------------------------------------------------
# for manufacturer in manufacturers_valve_type_data:
#     for valve_type in manufacturers_valve_type_data[manufacturer]:
#         output_file_path = os.path.join(result_manufacturer_valve_type_folder_path, manufacturer)
#         if not os.path.isdir(output_file_path):
#             os.makedirs(output_file_path, exist_ok=True)
#         output_file_path = os.path.join(
#             output_file_path, f"{valve_type}_analysis.png"
#         )
#         calculate_defect_intensivity(
#             manufacturers_valve_type_data[manufacturer][valve_type],
#             valve_type,
#             defect_type,
#             output_file_path,
#             NUMBER_OF_INTERVALS,
#             NUMBER_OF_ITEMS,
#             CONFIDENCE_LEVEL,
#         )
# --------------------------------------------------------------------------------------
