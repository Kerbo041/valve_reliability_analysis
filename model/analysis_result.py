from model.calculated_parameter import Calculated_parameter
from model.linear_regression import LinearRegression
from typing import List
class AnalysisResult():
    
    def __init__(self, 
                operating_time_intervals:List[Calculated_parameter],
                group_average_intensivity:List[float],
                average_intensivity:Calculated_parameter, 
                observation_average_intensivity:Calculated_parameter, 
                linear_regression:LinearRegression):
        
        self.operating_time_intervals = operating_time_intervals
        self.group_average_intensivity = group_average_intensivity
        self.average_intensivity = average_intensivity
        self.observation_average_intensivity = observation_average_intensivity
        self.linear_regression = linear_regression
        
        if not linear_regression.regression_values:
            linear_regression.calculate_regression_values(self.operating_time_intervals)