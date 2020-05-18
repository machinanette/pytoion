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

try:
    se = cube.SE._asdict()
    for key,value in se.items():
        print(key)
        cube.sound_effect(value)
        time.sleep(0.5)
finally:
    cube.disconnect()

