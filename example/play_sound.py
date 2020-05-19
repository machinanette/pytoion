import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import time
from pytoion import *

if len(sys.argv) == 1:
    print("Usage: python %s [BLE_DEVICE_ADDRESS]" %(sys.argv[0]))
    sys.exit()

cube = Toio(sys.argv[1])

# sound 
# see https://toio.github.io/toio-spec/docs/ble_sound

try:
    music1 = [
        cube.NOTE.C,
        cube.NOTE.CS,    # C#
        cube.NOTE.D,
        cube.NOTE.DS,
        cube.NOTE.E,
        cube.NOTE.F,
        cube.NOTE.FS,
        cube.NOTE.G,
        cube.NOTE.GS,
        cube.NOTE.A,
        cube.NOTE.AS,
        cube.NOTE.B,
    ]

    for note in music1:
        cube.sound(note)
        time.sleep(0.3)

    time.sleep(1)

    # [note, octave, time(time*10msec),volume(0:off/1-255:on)]
    music2= [
        [cube.NOTE.C,5,30],
        [cube.NOTE.D,5,50],
        [cube.NOTE.E,5,30],
        [cube.NOTE.F,5,50],
        [cube.NOTE.G,5,30],
        [cube.NOTE.A,5,50],
        [cube.NOTE.B,5,30],
        [cube.NOTE.C,6,50],
    ]

    for note in music2:
        cube.sound(*note)
        time.sleep(note[2]/100)

finally:
    cube.disconnect()

