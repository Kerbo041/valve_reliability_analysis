class DefectRecord:

    def __init__(
        self,
        number = None,
        valve_name=None,
        manufacturer=None,
        block_number=None,
        commissioning_date=None,
        defect_date=None,
        defect_time=None,
        defect_description=None,
        repair_date=None,
        repair_time=None,
    ):
        self.number = number
        self.valve_name = valve_name
        self.manufacturer = manufacturer
        self.commissioning_date = commissioning_date
        self.defect_date = defect_date
        self.defect_time = defect_time
        self.defect_description = defect_description
        self.block_number = block_number
        self.repair_date = repair_date
        self.repair_time = repair_time

    def __str__(self):
        return f"{self.number};{self.valve_name};{self.manufacturer};{self.block_number};{self.commissioning_date};{self.defect_date};"
