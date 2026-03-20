import enum

# from model.valve_execution_type_enum import ValveFunctionType


class ValveExecutionType(enum.Enum):

    default = "default"
    zadvijka = "Задвижка"
    klapan = "Клапан"
    armatura = "Арматура"
