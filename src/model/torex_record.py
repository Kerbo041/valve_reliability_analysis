class TorexRecord:

    def __init__(
        self,
        full_valve_name,
        description,
        valve_name_operational,
        valve_name_plant,
        block_number,
        valve_type_short,
        commissioning_date,
    ):
        self.full_valve_name = full_valve_name
        self.description = description
        self.valve_name_operational = valve_name_operational
        self.valve_name_plant = valve_name_plant
        self.block_number = block_number
        self.valve_type_short = valve_type_short
        self.commissioning_date = commissioning_date
    def __str__(self):
        # return  f"{self.full_valve_name};{self.description};{self.block_number};{self.commissioning_date};"
        return  f"{self.full_valve_name};{self.valve_name_plant};{self.valve_name_operational};"
    
    def get_block_number(self):
        return self.block_number.replace("БЛОК ", "")
    
    def get_valve_name_upper(self):
        if type(self.full_valve_name) is str:
            return self.full_valve_name.upper()
        else:
            return self.full_valve_name
    
    def get_valve_name_operational_upper(self):
        if type(self.valve_name_operational) is str:
            return self.valve_name_operational.upper()
        else:
            return self.valve_name_operational