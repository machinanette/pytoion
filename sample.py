import sys
import time
from pytoion import *

def main():

    cube = Toio(address)

    ## Battery charge
    print("battery", cube.battery()) 

    ## Button Status
    print(cube.button())

    ## Led
    cube.light_on(LedColor.RED)
    time.sleep(1)
    cube.light_off()

    cube.light_on(LedColor.GREEN, 255)

    ## Sound 

    ## Sound Effect
    cube.sound_effect(SoundEffect.GET_1)
    time.sleep(1)

    ## move 
    cube.forward()
    time.sleep(1)

    cube.back()
    time.sleep(1)

    cube.rotate_right()
    time.sleep(1)

    cube.rotate_left()
    time.sleep(1)

    cube.stop()

    # move position
    cube.move(250,250,50,45)
    print("pos:", cube.sense_position())

    cube.disconnect()

if __name__ == "__main__":
    if len(sys.argv) == 1:
      print('Usage: sample.py BLE_DEVICE_ADDRESS')
      sys.exit()
    address = sys.argv[1]

    main()
