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
    # [note, octave, time(time*10msec),volume(0:off/1-255:on)]

    music= [
        [cube.NOTE.D,5,100],
        [cube.NOTE.C,5,100],
        [cube.NOTE.D,5,100],
        [cube.NOTE.E,5,100],
        [cube.NOTE.G,5,100],
        [cube.NOTE.E,5,100],
        [cube.NOTE.D,5,150],
        [cube.NOTE.C,5,80,0],   # volume off
        [cube.NOTE.E,5,100],
        [cube.NOTE.G,5,100],
        [cube.NOTE.A,5,100],
        [cube.NOTE.G,5,50],
        [cube.NOTE.A,5,50],
        [cube.NOTE.D,6,100],
        [cube.NOTE.B,5,100],
        [cube.NOTE.A,5,100],
        [cube.NOTE.G,5,100],
        [cube.NOTE.C,5,60,0],
        [cube.NOTE.E,5,100],
        [cube.NOTE.G,5,100],
        [cube.NOTE.A,5,150],
        [cube.NOTE.C,5,80,0],
        [cube.NOTE.D,6,100],
        [cube.NOTE.C,6,100],
        [cube.NOTE.D,6,150],
        [cube.NOTE.C,5,80,0],
        [cube.NOTE.E,5,100],
        [cube.NOTE.G,5,100],
        [cube.NOTE.A,5,100],
        [cube.NOTE.G,5,100],
        [cube.NOTE.E,5,200],
        [cube.NOTE.G,5,50],
        [cube.NOTE.D,5,150],
        [cube.NOTE.C,5,80,0],
        [cube.NOTE.A,5,100],
        [cube.NOTE.C,6,100],
        [cube.NOTE.D,6,150],
        [cube.NOTE.C,5,80,0],
        [cube.NOTE.C,6,100],
        [cube.NOTE.D,6,100],
        [cube.NOTE.A,5,100],
        [cube.NOTE.G,5,100],
        [cube.NOTE.A,5,100],
        [cube.NOTE.G,5,50],
        [cube.NOTE.E,5,50],
        [cube.NOTE.D,5,150]
    ]

    for note in music:
        cube.sound(*note)
        time.sleep(note[2]/100)

finally:
    cube.disconnect()

