import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
from pytoion import *

if len(sys.argv) == 1:
    print("Usage: python %s [BLE_DEVICE_ADDRESS]" %(sys.argv[0]))
    sys.exit()

cube = Toio(sys.argv[1])

try:
    while True:
        cube.light_on(LedColor.RED)
        time.sleep(1)
        cube.light_off()
        time.sleep(1)
finally:
    cube.disconnect()

