class Defect:

    def __init__(
        self,
        number=None,
        defect_date=None,
        defect_time=None,
        defect_description=None,
        repair_date=None,
        repair_time=None,
        defect_type = None
    ):
        self.number = number
        self.defect_date = defect_date
        self.defect_time = defect_time
        self.defect_description = defect_description
        self.repair_date = repair_date
        self.repair_time = repair_time
        self.defect_type = defect_type

    def __str__(self):
        return f"{self.number};{self.defect_date};{self.defect_type}"
