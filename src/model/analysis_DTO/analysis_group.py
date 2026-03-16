from model.calculated_parameter import CalculatedParameter


class AnalysisGroup:

    def __init__(self, number_of_items, number_of_failures, average_operating_time):
        self.number_of_items = number_of_items
        self.number_of_failures = number_of_failures
        self.average_operating_time = average_operating_time

    def add_average_intensity(self, average_intensity: CalculatedParameter):
        self.average_intensity = average_intensity
