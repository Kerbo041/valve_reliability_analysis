from src.model.reader_DTO.valve import Valve
from typing import Dict, List, Tuple


def get_type_from_element_name(valve: Valve, whitelist: Dict[str, str]):
    result = False
    for main_type_name in whitelist:
        for type_name in whitelist[main_type_name]:
            for type_name_variant in whitelist[main_type_name][type_name]:
                if (
                    valve.valve_name
                    and valve.valve_name.upper().find(type_name_variant.upper()) != -1
                ):
                    result = True
                    valve.valve_type = type_name
                    valve.main_valve_type = main_type_name
                    return result
                if (
                    valve.element_name
                    and valve.element_name.upper().find(type_name_variant.upper()) != -1
                ):
                    result = True
                    valve.valve_type = type_name
                    valve.main_valve_type = main_type_name
                    return result
                if (
                    valve.get_descritpion()
                    and valve.get_descritpion().upper().find(type_name_variant.upper())
                    != -1
                ):
                    result = True
                    valve.valve_type = type_name
                    valve.main_valve_type = main_type_name
                    return result
        if (
            valve.valve_name
            and valve.valve_name.upper().find(main_type_name.upper()) != -1
        ):
            result = True
            valve.main_valve_type = main_type_name
            return result
        if (
            valve.element_name
            and valve.element_name.upper().find(main_type_name.upper()) != -1
        ):
            result = True
            valve.main_valve_type = main_type_name
            return result
        if (
            valve.get_descritpion()
            and valve.get_descritpion().upper().find(main_type_name.upper()) != -1
        ):
            result = True
            valve.main_valve_type = main_type_name
            return result
    return result


def filter_valves_by_name(valve: Valve, blacklist: List[str]):
    result = True
    for name in blacklist:
        if (
            valve.valve_name.upper().find(name.upper()) != -1
            or valve.element_name.upper().find(name.upper()) != -1
        ):
            result = False
            break
    return result
