from model.defect import Defect
from model.torex_record import TorexRecord
from typing import Dict, List, Tuple
from datetime import datetime


class Valve:

    def __init__(
        self,
        valve_name=None,
        manufacturer=None,
        block_number=None,
        commissioning_date=None,
        element_name=None,
        valve_type=None,  # Для дальнейшего определения
        main_valve_type=None,  # Для дальнейшего определения
        valve_type_short=None,  # ИЗ ТОРЭКС
        description=None,  # ИЗ ТОРЭКС
        valve_name_operational=None,  # ИЗ ТОРЭКС
        valve_name_plant=None,  # ИЗ ТОРЭКС
        full_valve_name=None,  # ИЗ ТОРЭКС
        manufacturer_defined=None # Для дальнейшего определения
    ):
        self.valve_name = valve_name
        self.manufacturer = manufacturer
        self.element_name = element_name
        self.set_block_number(block_number)
        try:
            self.commissioning_date = datetime.strptime(commissioning_date, "%d.%m.%Y")
        except:
            self.commissioning_date = None
        self.valve_type = valve_type
        self.main_valve_type = main_valve_type
        self.valve_type_short = valve_type_short  # ИЗ ТОРЭКС
        self.description = description  # ИЗ ТОРЭКС
        self.valve_name_operational = valve_name_operational  # ИЗ ТОРЭКС
        self.valve_name_plant = valve_name_plant  # ИЗ ТОРЭКС
        self.full_valve_name = full_valve_name  # ИЗ ТОРЭКС
        self.defect_list: List[Defect] = []
        self.manufacturer_defined = manufacturer_defined

    def add_defect(self, defect: Defect):
        self.defect_list.append(defect)

    def add_data_from_torex(self, torex_record: TorexRecord):
        self.description = torex_record.description
        self.valve_type_short = torex_record.valve_type_short
        self.valve_name_operational = torex_record.valve_name_operational
        self.valve_name_plant = torex_record.valve_name_plant
        self.full_valve_name = torex_record.full_valve_name

    def set_block_number(self, block_number):
        if block_number == "3; 4":
            self.block_number = "3-4"
        if block_number == "6; 7" or block_number == "6" or block_number == "7":
            self.block_number = "6-7"
        else:
            self.block_number = block_number
    def to_str_with_defects(self):
        output = f"{self.valve_name};{self.manufacturer};type: {self.valve_type};main type: {self.main_valve_type};description: {self.get_descritpion()};element_name: {self.element_name};{self.full_valve_name};{self.get_block_number()};{self.commissioning_date};"
        # if self.description:
        #     output += f"description:{self.description};"
        for iter, defect in enumerate(self.defect_list):
            output += f"{iter}: {defect}"
        return output
    def __str__(self):
        output = f"{self.valve_name};{self.full_valve_name};{self.get_block_number()};{self.valve_type};{self.main_valve_type}"
        return output


    def __eq__(self, value):
        if self.valve_name == value:
            return True
        else:
            return False

    def get_block_number(self):
        try:
            if int(self.block_number) == 3 or int(self.block_number) == 4:
                return "3-4"
            else:
                return self.block_number
        except Exception as e:
            return self.block_number

    def get_valve_name_upper(self):
        if type(self.valve_name) is str:
            return self.valve_name.upper()
        else:
            return self.valve_name

    def get_descritpion(self):
        if self.description is not None and self.description != "":
            return self.description
        elif type(self.full_valve_name) == str:
            if self.full_valve_name.upper() == self.valve_name.upper():
                return f"short_type: {self.valve_type_short};"
            else:
                return (
                    f"from_name: {self.full_valve_name.replace(self.valve_name, "")};"
                )
        else:
            return ""
