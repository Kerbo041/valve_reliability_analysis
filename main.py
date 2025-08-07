from defect_list_xslx_file_reader import *
from torex_xlsb_file_reader import *
from valve_type_search_in_torex import *
excel_file_path = "files\\Карта данных 2015-2025.xlsx"  # Укажите путь к вашему файлу
torex_file_path = "files\\Регистр ТОРЭКС_прореженный.xlsx"  # Укажите путь к вашему файлу

blacklist: List[str] = []

with open("files\\names_blaclist.txt", encoding="utf-8") as f:
    for line in f.readlines():
        blacklist.append(line.strip())

def filter_valves_by_name(valve:Valve, blacklist:List[str]):
    result = True
    for name in blacklist:
        if valve.valve_name.upper().find(name.upper()) != -1:
            result = False
    return result

workbook = openpyxl.load_workbook(excel_file_path)
sheet_names = workbook.sheetnames
column_names = read_column_names_from_json("column_names.json")
defect_list_file_data: List[List[Valve]] = []
for sheet_name in sheet_names:
    sheet = workbook[sheet_name]
    defect_list_file_data.append(get_defect_data_from_sheet(sheet, column_names))
# for i in defect_list_file_data:
#     with open("files\\defect_list.csv", "w",encoding="utf-8") as f:
#         for valve in i:
#             print(valve, file=f)
valve_list = {f"{valve.get_block_number()}_{valve.get_valve_name_upper()}": valve for valve in defect_list_file_data[0]}

workbook = openpyxl.load_workbook(torex_file_path)
sheet_names = workbook.sheetnames
column_names = read_column_names_from_json("column_names_torex.json")
torex_file_data:List[List[TorexRecord]] = []
for sheet_name in sheet_names:
    sheet = workbook[sheet_name]
    torex_file_data.append(get_torex_data_from_sheet(sheet, column_names))
# for i in torex_file_data:
#     with open("files\\torex.csv", "w",encoding="utf-8") as f:
#         for record in i:
#             print(record, file=f)
torex_list = {f"{torex_record.get_block_number()}_{torex_record.get_valve_name_operational_upper()}": torex_record for torex_record in torex_file_data[0]}

valve_type_search_in_torex(valve_list, torex_list)
file_valves_with_description = open("files\\valves_with_description.csv", "w",encoding="utf-8")
file_valves_without_description = open("files\\valves_without_description.csv", "w",encoding="utf-8")
file_not_valves = open("files\\not_valves.csv", "w",encoding="utf-8")

for valve_name in valve_list:
    if valve_list[valve_name].get_descritpion() is not None:
        print(valve_list[valve_name], file=file_valves_with_description)
    elif filter_valves_by_name(valve_list[valve_name], blacklist):
        print(valve_list[valve_name], file=file_valves_without_description)
    else:
        print(valve_list[valve_name], file=file_not_valves)
        
# with open("files\\c.csv", "w",encoding="utf-8") as f:
#         for valve_name in valve_list:
#             if valve_list[valve_name].get_descritpion() is not None:
#                 print(valve_list[valve_name], file=f)
# with open("files\\d.csv", "w",encoding="utf-8") as f:
#         for valve_name in valve_list:
#             if not valve_list[valve_name].get_descritpion():
#                 print(valve_list[valve_name], file=f)
