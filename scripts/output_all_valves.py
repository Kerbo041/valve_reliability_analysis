from model.valve import Valve
from typing import List, Dict, Tuple
from main import create_file

def output_all_valves(valve_list:Dict[str, Valve] , output_path = "files\\data\\all.csv"):
        
    file_valves_all = create_file(output_path)

    for valve_name in valve_list:
        print(valve_list[valve_name], file=file_valves_all)
