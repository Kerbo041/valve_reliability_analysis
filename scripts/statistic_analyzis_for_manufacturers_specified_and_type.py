import os
from calculate_defect_intensivity import get_analysis_result
from scripts.get_analyzis_for_filtered_4_with_VAB import *


# --------------------------------------------------------------------------------------
# Выполнение статистического анализа для разных производителей (распознанных из сырой таблицы) по типам арматуры
# --------------------------------------------------------------------------------------
def statistic_analyzis_for_manufacturers_specified_and_type(
    manufacturers_valve_type_data,
    result_manufacturer_valve_type_folder_path,
    NUMBER_OF_INTERVALS,
    NUMBER_OF_ITEMS,
    CONFIDENCE_LEVEL,
    vab,
):
    for manufacturer in manufacturers_valve_type_data:
        # for valve_type in manufacturers_valve_type_data[manufacturer]:
        #     output_file_path = os.path.join(result_manufacturer_valve_type_folder_path, manufacturer)
        #     if not os.path.isdir(output_file_path):
        #         os.makedirs(output_file_path, exist_ok=True)
        #     output_file_path = os.path.join(
        #         output_file_path, f"{valve_type}_analysis.png"
        #     )
        #     valve_type = None
        #     defect_type = None
        #     calculate_defect_intensivity(
        #         manufacturers_valve_type_data[manufacturer][valve_type],
        #         valve_type,
        #         defect_type,
        #         output_file_path,
        #         NUMBER_OF_INTERVALS,
        #         NUMBER_OF_ITEMS,
        #         CONFIDENCE_LEVEL,
        #     )
        if manufacturer is not None:
            base_path = "files//result_filtered_with_vab_and_manufacturer"
            base_path_with_manufacturer = os.path.join(base_path, manufacturer)
            get_analyzis_for_filtered_4(
                manufacturers_valve_type_data[manufacturer],
                NUMBER_OF_INTERVALS,
                NUMBER_OF_ITEMS,
                CONFIDENCE_LEVEL,
                vab,
                base_path_with_manufacturer,
            )


# --------------------------------------------------------------------------------------
