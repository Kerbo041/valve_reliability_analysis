import os
from typing import List, Dict, Tuple


def add_table_to_csv(table, rows_names, column_names, table_name):
    table_in_csv = ""
    if table_name:
        table_in_csv += f"{table_name}\n"
    if column_names:
        table_in_csv += ";"
        for name in column_names:
            table_in_csv += f"{name};"
        table_in_csv += "\n"

    for iter, row in enumerate(table):
        if type(rows_names) == type([]) and len(rows_names) >= iter:
            table_in_csv += f"{rows_names[iter]};"
        for value in row:
            table_in_csv += f"{str(value)};"
        table_in_csv += f"\n"
    return table_in_csv

def avg(list:List):
    try:
        if len(list) == 0:
            return 0
        else:
            return sum(list) / len(list)
    except:
        return 0

def output_statistic_analyzis_to_csv(
    file_name,
    data,
    avg_failure_rate,
    interval_width,
    intervals_borders,
    regression_line_slope,
    regression_line_intercept,
    failure_rates,
    counts_in_intervals,
    midpoints_of_intervals,
    сonfidence_interval_upper_border,
    сonfidence_interval_lower_border,
):
    count_of_defects = len(data)
    name_without_ext = os.path.splitext(file_name)[0]
    csv_file_data = f"{os.path.basename(name_without_ext)}\n"
    csv_file_data += f"кол-во дефектов;{count_of_defects}\n"
    csv_file_data += f"средняя интенсивность отказов;{avg_failure_rate}\n"
    csv_file_data += f"параметры интерполяции;a;{regression_line_slope}\n"
    csv_file_data += f";b;{regression_line_intercept}\n"
    interval_borders_table = [[], [], [], []]
    for iter in range(len(intervals_borders) - 1):
        interval_borders_table[0].append(iter + 1)
        interval_borders_table[1].append(intervals_borders[iter])
        interval_borders_table[2].append(intervals_borders[iter + 1])
        interval_borders_table[3].append(counts_in_intervals[iter])
    table_in_csv = add_table_to_csv(
        interval_borders_table,
        [
            "Номер интервала",
            "Граница нижняя, сут.",
            "Граница верхняя, сут.",
            "Кол-во отказов заданного типа",
        ],
        None,
        "Распределение отказов по наработке",
    )
    csv_file_data += table_in_csv



    work_in_intervals = [[] for i in range(10)]
    for value in data:
        for iter in range(len(intervals_borders)-1):
            if value >= intervals_borders[iter] and value <= intervals_borders[iter+1]:
                work_in_intervals[iter].append(value)
    avg_work_in_intervals = [avg(interval) for interval in work_in_intervals]
    avg_work_in_intervals_table = [[i for i in range(1, 11)], avg_work_in_intervals, failure_rates]
    table_in_csv = add_table_to_csv(
        avg_work_in_intervals_table,
        [
            "Номер интервала",
            "Средняя наработка в интервале, сут.",
            "Интенсивность отказов, 1/сут."
        ],
        None,
        "Распределение отказов по наработке",
    )
    csv_file_data += table_in_csv
    
    file_name = f"{name_without_ext}.csv"
    with open(file_name, "w") as csv_file:
        for row in csv_file_data:
            print(row, end="", file=csv_file)