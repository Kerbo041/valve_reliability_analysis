class TorexRecord:

    def __init__(
        self,
        valve_name,
        description,
        valve_name_operational,
        valve_name_plant,
        block_number,
        valve_type_short,
        commissioning_date,
    ):
        self.valve_name = valve_name
        self.description = description
        self.valve_name_operational = valve_name_operational
        self.valve_name_plant = valve_name_plant
        self.block_number = block_number
        self.valve_type_short = valve_type_short
        self.commissioning_date = commissioning_date
    def __str__(self):
        return  f"{self.valve_name};{self.description};{self.block_number};{self.commissioning_date};"