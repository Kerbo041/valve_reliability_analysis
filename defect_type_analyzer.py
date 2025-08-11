from model.valve import Valve
from model.defect import Defect
from typing import Dict, List, Tuple


def get_defect_type(valve: Valve, defect_names: Dict[str, List[str]]):
    for defect in valve.defect_list:
        searched_types = []
        for defect_type in defect_names:
            for defect_name_variant in defect_names[defect_type]:
                if defect.defect_type is None and defect.defect_description.upper().find(defect_name_variant.upper()) != -1:
                    searched_types.append(defect_type)
        if len(searched_types) > 0:
            defect.defect_type = searched_types[0]
            searched_types.pop(0)
        for defect_type in searched_types:
            new_defect = Defect(
                            number=defect.number,
                            defect_date=defect.defect_date,
                            defect_time=defect.defect_time,
                            defect_description=defect.defect_description,
                            repair_date=defect.repair_date,
                            repair_time=defect.repair_time,
                            defect_type=defect_type
                        )
            valve.add_defect(new_defect)
