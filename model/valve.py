from model.defect import Defect

class Defect:

    def __init__(
        self,
        defect_date=None,
        defect_time=None,
        defect_description=None,
        repair_date=None,
        repair_time=None,
    ):
        self.defect_date = defect_date
        self.defect_time = defect_time
        self.defect_description = defect_description
        self.repair_date = repair_date
        self.repair_time = repair_time


class Valve:

    def __init__(
        self,
        valve_name=None,
        manufacturer=None,
        block_number=None,
        commissioning_date=None,
        # valve_type=None,     # ИЗ ТОРЭКС
        # description=None,     # ИЗ ТОРЭКС
        # valve_name_operational=None,     # ИЗ ТОРЭКС
        # valve_name_plant=None,     # ИЗ ТОРЭКС
    ):
        self.valve_name = valve_name
        self.manufacturer = manufacturer
        self.block_number = block_number
        self.commissioning_date = commissioning_date
        # self.valve_type = valve_type                 # ИЗ ТОРЭКС
        # self.description = description                 # ИЗ ТОРЭКС
        # self.valve_name_operational = valve_name_operational                # ИЗ ТОРЭКС
        # self.valve_name_plant = valve_name_plant                # ИЗ ТОРЭКС
        self.defect_list = []
        
    def add_defect(self, defect: Defect):
        self.defect_list.append(defect)
    
    def __str__(self):
        output = f"{self.valve_name};{self.manufacturer};{self.block_number};{self.commissioning_date};"
        for iter, defect in enumerate(self.defect_list):
            output += f"{iter}: {defect}"
        return output
    
        
    def __eq__(self, value):
        if self.valve_name == value:
            return True
        else:
            return False