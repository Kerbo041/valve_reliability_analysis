import openpyxl
from json import load
from model.torex_record import TorexRecord
from typing import Dict, List, Tuple

def read_column_names_from_json(column_names_file_path):
    with open(column_names_file_path, encoding="utf-8") as column_names_file:
        column_names = load(column_names_file)
    return column_names


def get_torex_data_from_sheet(defects_list_sheet, column_names)-> List[TorexRecord]:
    header_row = list(
        defects_list_sheet.iter_rows(min_row=1, max_row=1, values_only=True)
    )[0]
    column_numbers = get_column_numbers(column_names, header_row)
    defect_records_list = []
    for row in defects_list_sheet.iter_rows(min_row=1, values_only=True):
        defect_records_list.append(get_torex_record_from_xlsx_row(row, column_numbers))
    return defect_records_list


def get_column_numbers(column_names: Dict[str,str], header_row: Tuple[str]):
    """Получение номеров столбцов по их названиям.
    
    Args:
        column_names (dict): Словарь с названиями столбцов в формате {ключ: название}.
        header_row (tuple): Кортеж с названиями столбцов из заголовка таблицы.
    
    Returns:
        dict: Словарь с номерами столбцов в формате {ключ: номер}.
    
    Raises:
        Exception: Если какой-то из столбцов не найден в заголовке.
    """
    try:
        # Создание словаря {ключ: номер_столбца}
        column_numbers = {
            key: header_row.index(column_names[key]) for key in column_names
        }
        return column_numbers
    except Exception as exception:
        pass
    missing_columns = [name for name in column_names.values() if name not in header_row]
    if missing_columns:
        raise ValueError(f"Столбцы не найдены: {', '.join(missing_columns)}")
    return {key: header_row.index(name) for key, name in column_names.items()}


def get_torex_record_from_xlsx_row(defect_list_row, column_numbers):
    record_data = {}
    for key in column_numbers:
        record_data[key] = defect_list_row[column_numbers[key]]
    return TorexRecord(
        full_valve_name = record_data["full_valve_name"],
        description = record_data["description"],
        valve_name_operational = record_data["valve_name_operational"],
        valve_name_plant = record_data["valve_name_plant"],
        block_number = record_data["block_number"],
        valve_type_short = record_data["valve_type_short"],
        commissioning_date = record_data["commissioning_date"]
    )
