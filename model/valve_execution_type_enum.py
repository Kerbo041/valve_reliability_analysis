import enum
from model.valve_execution_type_enum import ValveFunctionType


class ValveExecutionType(enum.Enum):

    zadvijka = "Задвижка"
    klapan = "Клапан"
    armatura = "Арматура"
