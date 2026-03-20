from src.model.reader_DTO.valve import Valve
from src.model.reader_DTO.torex_record import TorexRecord
from typing import Dict, List, Tuple


def valve_type_search_in_torex(
    valve_list: Dict[str, Valve], torex_list: Dict[str, TorexRecord]
):
    for valve_name in valve_list:
        if valve_name in torex_list:
            valve_list[valve_name].add_data_from_torex(torex_list[valve_name])
