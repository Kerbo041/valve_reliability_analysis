import openpyxl
from json import load
from model.defect import Defect
from model.valve import Valve
from typing import Dict, List, Tuple

"""
Модуль для парсинга данных о дефектах из Excel.

"""

def read_column_names_from_json(column_names_file_path:str) -> Dict[str, str]:
    """Чтение названий столбцов из JSON-файла.
    
    Args:
        column_names_file_path (str): Путь к JSON-файлу с названиями столбцов.
    
    Returns:
        dict: Словарь с названиями столбцов.
    """
    with open(column_names_file_path, encoding="utf-8") as column_names_file:
        column_names = load(column_names_file)
    return column_names


def get_defect_data_from_sheet(defects_list_sheet, column_names):
    """Извлечение данных о дефектах из листа Excel.
    
    Args:
        defects_list_sheet (Worksheet): Лист Excel с данными о дефектах.
        column_names (dict): Словарь с названиями столбцов.
    
    Returns:
        list[Valve]: Список объектов Valve с информацией о дефектах.
    """
    valve_list: List[Valve] = []
    # Получение заголовков таблицы (первая строка)
    header_row = list(
        defects_list_sheet.iter_rows(min_row=1, max_row=1, values_only=True)
    )[0]
    # Получение номеров столбцов по их названиям
    column_numbers = get_column_numbers(column_names, header_row)
    # Обработка каждой строки таблицы, начиная со второй
    for row in defects_list_sheet.iter_rows(min_row=2, values_only=True):
        get_defect_record_from_xlsx_row(valve_list, row, column_numbers)
    return valve_list


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


def get_defect_record_from_xlsx_row(valve_list, defect_list_row, column_numbers):
    """ Обработка строки таблицы и добавление информации о дефекте в список арматур.
    Функция анализирует строку таблицы, извлекает данные о дефекте и добавляет их
    в соответствующий объект Valve. Если арматура с указанным именем не найдена,
    создается новый объект Valve.
    Args:
        valve_list (array): список всех прочитанных арматур из таблицы
        defect_list_row (tuple): кортеж с ячейками изпрочитанной строки таблицы
        column_numbers (dict): словарь из необходимых столбцов и их номеров в таблице
    
    """
    # Извлечение данных из строки по номерам столбцов
    record_data = {}
    for key in column_numbers:
        record_data[key] = defect_list_row[column_numbers[key]]
    # попытка найти арматуру из прочитанной строки в списке арматур 
    # при отсутствии возникает ValueError, при этом результатом поиска выводится False 
    try:
        valve_list_index = valve_list.index(record_data["valve_name"])
    except Exception as e:
        valve_list_index = False
    # извлечение записи о дефекте из строки
    new_defect = Defect(
        number = record_data["number"],
        defect_date=record_data["defect_date"],
        defect_time=record_data["defect_time"],
        defect_description=record_data["defect_description"],
        repair_date=record_data["repair_date"],
        repair_time=record_data["repair_time"],
    )
    # если арматура найдена, то дефект добавляется к ней
    if valve_list_index:
        valve_list[valve_list_index].add_defect(new_defect)
    else:
    # если не найдена, то создается новая, к ней добавляется дефект
    # и новая арматура заносится в выходной список
        new_valve = Valve(
            valve_name=record_data["valve_name"],
            manufacturer=record_data["manufacturer"],
            block_number=record_data["block_number"],
            commissioning_date=record_data["commissioning_date"],
        )
        new_valve.add_defect(new_defect)
        valve_list.append(new_valve)
