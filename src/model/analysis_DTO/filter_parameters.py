from typing import List, Dict, Tuple


class FilterParameters:

    def __init__(
        self,
        functional_type_array: List[str],
        construction_type_array: List[str],
        block_number_array: List[str],
    ):
        self.functional_type_array = functional_type_array
        self.construction_type_array = construction_type_array
        self.block_number_array = block_number_array
