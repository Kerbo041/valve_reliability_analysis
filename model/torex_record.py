class TorexRecord:

    def __init__(
        self,
        valve_name,
        description,
        valve_name_operational,
        valve_name_plant,
        block_number,
        valve_class,
        commissioning_date,
    ):
        self.valve_name = valve_name
        self.description = description
        self.valve_name_operational = valve_name_operational
        self.valve_name_plant = valve_name_plant
        self.block_number = block_number
        self.valve_class = valve_class
        self.commissioning_date = commissioning_date
