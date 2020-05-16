import sys
import bluepy
import time

# LED COLOR
class LedColor:
    RED = [255, 0, 0]
    GREEN = [ 0, 255, 0]
    BLUE = [ 0, 0, 255]

# SOUND EFFECT
class SoundEffect:
    ENTER = 0
    SELECTED = 1
    CANCEL = 2
    CURSOR = 3
    MAT_IN = 4
    MAT_OUT = 5
    GET_1 = 6
    GET_2 = 7
    GET_3 = 8
    EFFECT_1 = 9
    EFFECT_2 = 10

# CHARACTERISTIC uuid and handle
class Characteristic:
    uuid_dic = {
        "00002a00": "DEVICE_NAME",
        "00002a01": "APPEARANCE",
        "00002a04": "PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS",
        "00002aa6": "CENTRAL_ADDRESS_RESOLUTION",
        "10b20101": "ID_INFORMATION",
        "10b20102": "MOTOR_CONTROL",
        "10b20103": "LIGHT_CONTROL",
        "10b20104": "SOUND_CONTROL",
        "10b20106": "SENSOR_INFORMATION",
        "10b20107": "BUTTON_INFORMATION",
        "10b20108": "BATTERY_INFORMATION",
        "10b201ff": "CONFIGURATION"
    }

    def __init__(self, peripheral):
        self.__set_handle_id(peripheral)

    def __set_handle_id(self, peripheral):
        charas = peripheral.getCharacteristics()

        for chara in charas:
            key = str(chara.uuid).split("-")[0]
            if(key in self.uuid_dic):
                exec("self.{}={}".format(self.uuid_dic[key],chara.getHandle()))

class Toio:
    def __init__(self, address):
        self.address = address

        try:
            self.peripheral = bluepy.btle.Peripheral()
            self.peripheral.connect(self.address, bluepy.btle.ADDR_TYPE_RANDOM)
        except:
            print("device connection failed")
            sys.exit()

        self.HANDLE = Characteristic(self.peripheral)

    def button(self):
        status = {0x80 : "ON", 0x00 : "OFF"}
        ret = ""

        try:
            btn = self.peripheral.readCharacteristic(
                self.HANDLE.BUTTON_INFORMATION)
            ret = status[btn[1]]
        except:
            return False

        return ret

    def battery(self):
        try:
            bat = self.peripheral.readCharacteristic(
                self.HANDLE.BATTERY_INFORMATION)
        except:
            return False

        return ord(bat)

    def disconnect(self):
        try:
            self.peripheral.disconnect()
        except:
            return False

    def light_on(self, color, time = 0):

        data = [3, time, 1, 1] + color

        try:
            self.peripheral.writeCharacteristic(
                self.HANDLE.LIGHT_CONTROL,
                bytearray(data),
			    True)
        except:
            return False

        return True

    def light_off(self):
        try:
            self.peripheral.writeCharacteristic(
                self.HANDLE.LIGHT_CONTROL,
                bytes([1]),
                True)
        except:
            return False

        return True

    def sound_effect(self, type):
        data = [2, type, 255]
        self.peripheral.writeCharacteristic(
            self.HANDLE.SOUND_CONTROL,
            bytearray(data),
            True)

        return True

    def sound(self):
        pass

    def __control_motor(self, left_motor, right_motor):
        data = [1] + left_motor + right_motor

        try:
            self.peripheral.writeCharacteristic(
                self.HANDLE.MOTOR_CONTROL,
                bytearray(data),
                True)
        except:
            return False

        return True

    def forward(self, speed = 50):
        return self.__control_motor([1, 1, speed],[2, 1, speed])

    def back(self, speed = 50):
        return self.__control_motor([1, 2, speed],[2, 2, speed])

    def stop(self):
        return self.__control_motor([1, 1, 0],[2, 1, 0])

    def rotate_left(self, speed = 50, operating_time = 0.05):
        ret =  self.__control_motor([1, 2, speed],[2, 1, speed])
        if(ret == True):
            time.sleep(operating_time)
            self.stop()

        return ret

    def rotate_right(self, speed = 50, operating_time = 0.05):
        ret = self.__control_motor([1, 1, speed],[2, 2, speed])

        if(ret == True):
            time.sleep(operating_time)
            self.stop()

        return ret

    def forward_pos(self):
        pass

    def back_pos(self):
        pass

    def rotate_left_pos(self):
        pass

    def pos_rotate_pos(self):
        pass

    def move(self):
        pass


    def double_tap(self):
        pass

    def collision(self):
        pass

    def level(self):
        pass

    def attitude(self):
        pass

    def position(self):
        pass

def main():
    pass

if __name__ == "__main__":
    main()
