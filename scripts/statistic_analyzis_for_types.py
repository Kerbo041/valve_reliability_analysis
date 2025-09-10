import os
from calculate_defect_intensivity import calculate_defect_intensivity

# --------------------------------------------------------------------------------------
# Выполнение статистического анализа для разных типов арматур и дефектов
# --------------------------------------------------------------------------------------
def statistic_analyzis_for_types(
    defect_array_output,
    result_folder_path,
    NUMBER_OF_INTERVALS,
    NUMBER_OF_ITEMS,
    CONFIDENCE_LEVEL,
):
    for valve_type in defect_array_output:
        for defect_type in defect_array_output[valve_type]:
            output_file_path = os.path.join(result_folder_path, valve_type)
            if not os.path.isdir(output_file_path):
                os.makedirs(output_file_path, exist_ok=True)
            output_file_path = os.path.join(
                output_file_path, f"{valve_type}_{defect_type}_analysis.png"
            )
            calculate_defect_intensivity(
                defect_array_output[valve_type][defect_type],
                valve_type,
                defect_type,
                output_file_path,
                NUMBER_OF_INTERVALS,
                NUMBER_OF_ITEMS,
                CONFIDENCE_LEVEL,
            )


# --------------------------------------------------------------------------------------
