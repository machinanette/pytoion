import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
from pytoion import *

if len(sys.argv) == 1:
    print("Usage: python %s [BLE_DEVICE_ADDRESS]" %(sys.argv[0]))
    sys.exit()

cube = Toio(sys.argv[1])

cube.led_on(cube.COLOR.GREEN)
time.sleep(1)
cube.led_off()

try:
    while True:
        color = cube.COLOR._asdict()
        for key,value in color.items():
            print("blink: ", key)
            cube.led_on(value)
            time.sleep(1)
            cube.led_off()
finally:
    cube.led_off()
    cube.disconnect()

