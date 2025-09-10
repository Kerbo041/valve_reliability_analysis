import os
from calculate_defect_intensivity import calculate_defect_intensivity


# --------------------------------------------------------------------------------------
# Выполнение статистического анализа для разных производителей (распознанных из сырой таблицы)
# --------------------------------------------------------------------------------------
def statistic_analyzis_for_manufacturers_specified(
    manufacturers_defined_data,
    result_manufacturer_defined_folder_path,
    NUMBER_OF_INTERVALS,
    NUMBER_OF_ITEMS,
    CONFIDENCE_LEVEL,
):
    for manufacturer in manufacturers_defined_data:
        result_file_path = result_manufacturer_defined_folder_path
        if not os.path.isdir(result_file_path):
            os.makedirs(result_file_path, exist_ok=True)
        result_file_path = os.path.join(
            result_file_path, f"{manufacturer}_analysis.png"
        )
        valve_type = None
        defect_type = None
        calculate_defect_intensivity(
            manufacturers_defined_data[manufacturer],
            valve_type,
            defect_type,
            result_file_path,
            NUMBER_OF_INTERVALS,
            NUMBER_OF_ITEMS,
            CONFIDENCE_LEVEL,
        )
# --------------------------------------------------------------------------------------
