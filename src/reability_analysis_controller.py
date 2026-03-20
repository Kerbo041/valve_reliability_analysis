from reabitlity_analysis.make_analysis import make_analysis
from typing import List, Dict, Tuple
from src.model.analysis_DTO.filter_parameters import FilterParameters
from src.model.analysis_DTO.analysis_parameters import AnalysisParameters
from src.model.analysis_DTO.analysis import Analysis


def create_analysis(
    filter_parameters: FilterParameters, analysis_parameters: AnalysisParameters
):
    analysis = Analysis()

    selected_data = None  # filters
