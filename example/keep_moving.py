import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
from pytoion import *

if len(sys.argv) == 1:
    print("Usage: python %s [BLE_DEVICE_ADDRESS]" %(sys.argv[0]))
    sys.exit()

cube = Toio(sys.argv[1])

# keep moving until call stop function
try:
    while True:
        cube.forward()
        time.sleep(0.3)
        cube.rotate_right()
        time.sleep(0.3)
        cube.rotate_left()
        time.sleep(0.3)
        cube.back()
        time.sleep(0.3)
finally:
    cube.stop()
    cube.disconnect()

