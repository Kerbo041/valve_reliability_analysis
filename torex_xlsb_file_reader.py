excel_file_path = "files\\Карта данных 2015-2025.xlsx"  # Укажите путь к вашему файлу
torex_file_path = "files\\Регистр ТОРЭКС_прореженный.xlsb"  # Укажите путь к вашему файлу

import openpyxl
from json import load

# from datetime import datetime, timedelta
# import os
from model.defect_record import DefectRecord


def read_column_names_from_json(column_names_file_path):
    with open(column_names_file_path, encoding="utf-8") as column_names_file:
        column_names = load(column_names_file)
    return column_names


def get_data_from_sheet(defects_list_sheet, column_names):
    header_row = list(
        defects_list_sheet.iter_rows(min_row=1, max_row=1, values_only=True)
    )[0]
    column_numbers = get_column_numbers(column_names, header_row)
    defect_records_list = []
    for row in defects_list_sheet.iter_rows(min_row=2, values_only=True):
        defect_records_list.append(get_defect_record_from_xlsx_row(row, column_numbers))
    return defect_records_list


def get_column_numbers(column_names, header_row):
    try:
        column_numbers = {
            key: header_row.index(column_names[key]) for key in column_names
        }
        return column_numbers
    except Exception as exception:
        raise


def get_defect_record_from_xlsx_row(defect_list_row, column_numbers):
    record_data = {}
    for key in column_numbers:
        record_data[key] = defect_list_row[column_numbers[key]]
    return DefectRecord(
        number = record_data["number"],
        valve_name=record_data["valve_name"],
        manufacturer=record_data["manufacturer"],
        block_number=record_data["block_number"],
        commissioning_date=record_data["commissioning_date"],
        defect_date=record_data["defect_date"],
        defect_time=record_data["defect_time"],
        defect_description=record_data["defect_description"],
        repair_date=record_data["repair_date"],
        repair_time=record_data["repair_time"],
    )


workbook = openpyxl.load_workbook(torex_file_path)
sheet_names = workbook.sheetnames
column_names = read_column_names_from_json("column_names_torex.json")
file_data = []
for sheet_name in sheet_names:
    sheet = workbook[sheet_name]
    file_data.append(get_data_from_sheet(sheet, column_names))
for i in file_data:
    with open("a.csv", "w",encoding="utf-8") as f:
        for record in i:
            print(record, file=f)

#     for row in sheet.iter_rows(min_row=2, values_only=True):
#         defect_type = row[0]
#         block_number = row[3]
#         value = (row[4] - row[2]).days
#         if not defect_type in file_data[sheet_name][folder_name_by_type].keys():
#             file_data[sheet_name][folder_name_by_type][defect_type] = []
#         file_data[sheet_name][folder_name_by_type][defect_type].append(value)

#         if not block_number in file_data[sheet_name][folder_name_by_block_number].keys():
#             file_data[sheet_name][folder_name_by_block_number][block_number] = {}
#         if not defect_type in file_data[sheet_name][folder_name_by_block_number][block_number].keys():
#             file_data[sheet_name][folder_name_by_block_number][block_number][defect_type] = []
#         file_data[sheet_name][folder_name_by_block_number][block_number][defect_type].append(value)
# workbook.close()

# for sheet_name in sheet_names:
#     for defect_type in file_data[sheet_name][folder_name_by_type]:
#         file_name = f"данные {defect_type}.txt"
#         defect_name = f"отказ {sheet_name.lower()}"
#         folder_path = os.path.join(folder_for_txt_path,defect_name, folder_name_by_type)
#         write_file(folder_path, file_name, file_data[sheet_name][folder_name_by_type][defect_type])

#     for block_number in file_data[sheet_name][folder_name_by_block_number]:
#         for defect_type in file_data[sheet_name][folder_name_by_block_number][block_number]:
#             file_name = f"данные {defect_type}.txt"
#             defect_name = f"отказ {sheet_name.lower()}"
#             folder_path = os.path.join(folder_for_txt_path, defect_name, folder_name_by_block_number, block_number)
#             write_file(folder_path, file_name, file_data[sheet_name][folder_name_by_block_number][block_number][defect_type])
