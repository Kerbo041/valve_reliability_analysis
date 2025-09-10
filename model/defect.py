from datetime import datetime

class Defect:

    def __init__(
        self,
        number=None,
        defect_date=None,
        defect_time=None,
        defect_description=None,
        repair_date=None,
        repair_time=None,
        defect_type = None,
        defect_class = None
    ):
        self.number = number
        try:
            if type(defect_date) == datetime:
                self.defect_date = defect_date
            else:
                self.defect_date = datetime.strptime(defect_date, "%d.%m.%Y")
        except:
            self.defect_date = None
        self.defect_time = defect_time
        self.defect_description = defect_description
        self.repair_date = repair_date
        self.repair_time = repair_time
        self.defect_type = defect_type
        self.defect_class = defect_class

    def __str__(self):
        return f"{self.number};{self.defect_date};{self.defect_type};"
