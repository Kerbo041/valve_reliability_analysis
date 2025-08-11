from defect_list_xslx_file_reader import get_defect_data_from_sheet
from torex_xlsb_file_reader import get_torex_data_from_sheet
from valve_type_search_in_torex import valve_type_search_in_torex
from valve_type_analyzer import get_type_from_element_name, filter_valves_by_name
from defect_type_analyzer import get_defect_type
from model.valve import Valve, Defect
from model.torex_record import TorexRecord
from json import load
from typing import Dict, List, Tuple
import openpyxl

excel_file_path = "files\\данные\\Карта данных 2015-2025.xlsx"  # Укажите путь к вашему файлу
torex_file_path = (
    "files\\данные\\Регистр ТОРЭКС_прореженный.xlsx"  # Укажите путь к вашему файлу
)


def check_valve_type(valve: Valve):
    result = False
    if valve.valve_type is not None and valve.main_valve_type is not None:
        if valve.valve_type.upper().find(valve.main_valve_type.upper()) == -1 or (
            valve.get_descritpion() != ""
            and valve.get_descritpion().find(valve.main_valve_type.upper()) == -1
        ):
            result = True
    return result


blacklist: List[str] = []

with open("files\\settings\\names_blacklist.txt", encoding="utf-8") as f:
    for line in f.readlines():
        blacklist.append(line.strip())


with open("files\\settings\\names_whitelist.json", encoding="utf-8") as whitelist_file:
    whitelist = load(whitelist_file)

with open("files\\settings\\defect_list.json", encoding="utf-8") as defect_types_file:
    defect_types = load(defect_types_file)

with open("column_names.json", encoding="utf-8") as column_names_file:
    column_names = load(column_names_file)
with open("column_names_torex.json", encoding="utf-8") as column_names_file:
    column_names_torex = load(column_names_file)

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

valve_type_search_in_torex(valve_list, torex_list)
file_valves_with_description = open(
    "files\\data\\valves_with_description.csv", "w", encoding="utf-8"
)
file_valves_with_type = open("files\\valves_with_type.csv", "w", encoding="utf-8")
file_valves_without_description = open(
    "files\\data\\valves_without_description.csv", "w", encoding="utf-8"
)
file_valves_with_main_type = open(
    "files\\data\\valves_with_main_type.csv", "w", encoding="utf-8"
)
file_valves_error_type = open("files\\data\\valves_error_type.csv", "w", encoding="utf-8")
file_not_valves = open("files\\data\\not_valves.csv", "w", encoding="utf-8")
file_not_valves = open("files\\data\\not_valves.csv", "w", encoding="utf-8")
file_result_for_valves_leak  = open("files\\output\\valves_leak.txt", "w", encoding="utf-8")
file_result_for_valves_crack  = open("files\\output\\valves_crack.txt", "w", encoding="utf-8")
file_result_for_valves_pass  = open("files\\output\\valves_pass.txt", "w", encoding="utf-8")
file_result_for_valves_error  = open("files\\output\\valves_error.txt", "w", encoding="utf-8")
file_result_for_valves_no_defect_type  = open("files\\output\\valves_no_defect_type.txt", "w", encoding="utf-8")

for valve_name in valve_list:
    get_type_from_element_name(valve_list[valve_name], whitelist)
    get_defect_type(valve_list[valve_name], defect_types)
    # if check_valve_type(valve_list[valve_name]):
    #     print(valve_list[valve_name], file=file_valves_error_type)
    if valve_list[valve_name].get_descritpion() != "":
        print(valve_list[valve_name], file=file_valves_with_description)
    elif valve_list[valve_name].valve_type is not None:
        print(valve_list[valve_name], file=file_valves_with_type)
    elif valve_list[valve_name].main_valve_type is not None:
        print(valve_list[valve_name], file=file_valves_with_main_type)
    elif filter_valves_by_name(valve_list[valve_name], blacklist):
        print(valve_list[valve_name], file=file_valves_without_description)
    else:
        print(valve_list[valve_name], file=file_not_valves)
    if valve_list[valve_name].main_valve_type == "Задвижка":
        if valve_list[valve_name].commissioning_date is not None:
            for defect in valve_list[valve_name].defect_list:
                if defect.defect_date is not None:
                    try:
                        if defect.defect_type == None:
                            print(valve_list[valve_name], file=file_result_for_valves_no_defect_type)
                            print(defect, file=file_result_for_valves_no_defect_type)
                        elif defect.defect_type.upper() == "ТЕЧЬ":
                            print((defect.defect_date - valve_list[valve_name].commissioning_date).days, file=file_result_for_valves_leak)
                        elif defect.defect_type.upper() == "ТРЕЩИНА":
                            print((defect.defect_date - valve_list[valve_name].commissioning_date).days, file=file_result_for_valves_crack)
                        elif defect.defect_type.upper() == "ПРОПУСК":
                            print((defect.defect_date - valve_list[valve_name].commissioning_date).days, file=file_result_for_valves_pass)
                    except:
                        print(valve_list[valve_name], file=file_result_for_valves_error)
                        print(defect, file=file_result_for_valves_error)
                        print("error with defect type/time", file=file_result_for_valves_error)
                else:
                    print(valve_list[valve_name], file=file_result_for_valves_error)
                    print("no defect time", file=file_result_for_valves_error)
        else:
            print(valve_list[valve_name], file=file_result_for_valves_error)
            print("no commissioning time", file=file_result_for_valves_error)
            
# with open("files\\c.csv", "w",encoding="utf-8") as f:
#         for valve_name in valve_list:
#             if valve_list[valve_name].get_descritpion() is not None:
#                 print(valve_list[valve_name], file=f)
# with open("files\\d.csv", "w",encoding="utf-8") as f:
#         for valve_name in valve_list:
#             if not valve_list[valve_name].get_descritpion():
#                 print(valve_list[valve_name], file=f)
