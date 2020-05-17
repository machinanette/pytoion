import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pytoion import *

if len(sys.argv) == 1:
    print("Usage: python %s [BLE_DEVICE_ADDRESS]" %(sys.argv[0]))
    sys.exit()

cube = Toio(sys.argv[1])

try:
    print("battery %d%%" % cube.battery())
finally:
    cube.disconnect()

