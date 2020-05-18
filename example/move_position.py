import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pytoion import *

if len(sys.argv) == 1:
    print("Usage: python %s [BLE_DEVICE_ADDRESS]" %(sys.argv[0]))
    sys.exit()

# required : mat for development
#
# move(X, Y, stop_angle, speed, move_type)
# rotate(direction, angle, speed)
#
# speed : 10..255
# stop_angle : https://toio.github.io/toio-spec/docs/ble_id#%E8%A7%92%E5%BA%A6
# rotate_type : https://toio.github.io/toio-spec/docs/ble_motor#%E7%A7%BB%E5%8B%95%E3%82%BF%E3%82%A4%E3%83%97

cube = Toio(sys.argv[1])

try:
    while True:
        # move center position and start
        ret = cube.move(250,250)
        print(ret)
        cube.rotate("left",180)
        cube.move(200,250)
        cube.rotate("right",45)
        cube.move(250,300,315)
        cube.move(300,250,225)
        cube.move(250,200,90,100)
finally:
    cube.disconnect()

