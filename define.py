from typing import NamedTuple, TypedDict

# LED COLOR PATTERN
class LedColor(NamedTuple):
    RED:    tuple = (255, 0, 0)
    GREEN:  tuple = (0, 255, 0)
    BLUE:   tuple = (0, 0, 255)
    YELLOW: tuple = (255, 255, 0)
    PURPLE: tuple = (255, 0, 255)
    AQUA:   tuple = (0, 255, 255)
    WHITE:  tuple = (255, 255, 255)

# SOUND EFFECT LIST
class SoundEffect(NamedTuple):
    ENTER:    int = 0
    SELECTED: int = 1
    CANCEL:   int = 2
    CURSOR:   int = 3
    MAT_IN:   int = 4
    MAT_OUT:  int = 5
    GET_1:    int = 6
    GET_2:    int = 7
    GET_3:    int = 8
    EFFECT_1: int = 9
    EFFECT_2: int = 10

# CHARACTERISTIC LIST(HANDLE ID LIST)
class Characteristic(NamedTuple):
    DEVICE_NAME: int = 0
    APPEARANCE: int = 0
    PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS: int = 0
    CENTRAL_ADDRESS_RESOLUTION: int = 0
    ID_INFORMATION: int = 0
    MOTOR_CONTROL: int = 0
    LIGHT_CONTROL: int = 0
    SOUND_CONTROL: int = 0
    SENSOR_INFORMATION: int = 0
    BUTTON_INFORMATION: int = 0
    BATTERY_INFORMATION: int = 0
    CONFIGURATION: int = 0

    UUID_DIC : dict = {
        "00002a00": "DEVICE_NAME",
        "00002a01": "APPEARANCE",
        "00002a04": "PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS",
        "00002aa6": "CENTRAL_ADDRESS_RESOLUTION",
        "10b20101": "ID_INFORMATION",
        "10b20102": "MOTOR_CONTROL",
        "10b20103": "LIGHT_CONTROL",
        "10b20104": "SOUND_CONTROL",
        "10b20106": "SENSOR_INFORMATION",
        "10b20107": "BUTTON_INFORMATION",
        "10b20108": "BATTERY_INFORMATION",
        "10b201ff": "CONFIGURATION"
    }

# SOUND
class Sound(NamedTuple):
    C:  int = 0
    CS: int = 1
    D:  int = 2
    DS: int = 3
    E:  int = 4
    F:  int = 5
    FS: int = 6
    G:  int = 7
    GS: int = 8
    A:  int = 9
    AS: int = 10
    B:  int = 11

