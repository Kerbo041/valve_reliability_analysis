from defect_list_xslx_file_reader import *
from torex_xlsb_file_reader import *
excel_file_path = "files\\Карта данных 2015-2025.xlsx"  # Укажите путь к вашему файлу
torex_file_path = "files\\Регистр ТОРЭКС_прореженный.xlsx"  # Укажите путь к вашему файлу

workbook = openpyxl.load_workbook(excel_file_path)
sheet_names = workbook.sheetnames
column_names = read_column_names_from_json("column_names.json")
defect_list_file_data = []
for sheet_name in sheet_names:
    sheet = workbook[sheet_name]
    defect_list_file_data.append(get_defect_data_from_sheet(sheet, column_names))
for i in defect_list_file_data:
    with open("files\\a.csv", "w",encoding="utf-8") as f:
        for valve in i:
            print(valve, file=f)


workbook = openpyxl.load_workbook(torex_file_path)
sheet_names = workbook.sheetnames
column_names = read_column_names_from_json("column_names_torex.json")
file_data = []
for sheet_name in sheet_names:
    sheet = workbook[sheet_name]
    file_data.append(get_torex_data_from_sheet(sheet, column_names))
for i in file_data:
    with open("files\\b.csv", "w",encoding="utf-8") as f:
        for record in i:
            print(record, file=f)