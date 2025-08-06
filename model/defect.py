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
    
    def __str__(self):
        return f"{self.defect_date};"