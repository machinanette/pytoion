import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
from pytoion import *

if len(sys.argv) == 1:
    print("Usage: python %s [BLE_DEVICE_ADDRESS]" %(sys.argv[0]))
    sys.exit()

cube = Toio(sys.argv[1])

# preset sound effect
# see https://toio.github.io/toio-spec/docs/ble_sound
se = {
    "Enter"    : SoundEffect.ENTER,
    "Selected" : SoundEffect.SELECTED,
    "Cancel"   : SoundEffect.CANCEL,
    "Cursor"   : SoundEffect.CURSOR,
    "Mat in"   : SoundEffect.MAT_IN,
    "Mat Out"  : SoundEffect.MAT_OUT,
    "Get 1"    : SoundEffect.GET_1,
    "Get 2"    : SoundEffect.GET_2,
    "Get 3"    : SoundEffect.GET_3,
    "Effect 1" : SoundEffect.EFFECT_1,
    "Effect 2" : SoundEffect.EFFECT_2
}

try:
    for key,value in se.items():
        print(key)
        cube.sound_effect(value)
        time.sleep(1)
finally:
    cube.disconnect()

