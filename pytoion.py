import bluepy
import time
import struct
import queue

# LED COLOR PATTERN
class LedColor:
    RED = [255, 0, 0]
    GREEN = [ 0, 255, 0]
    BLUE = [ 0, 0, 255]

# SOUND EFFECT LIST
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

# CHARACTERISTIC UUID LIST
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

class ToioDelegate(bluepy.btle.DefaultDelegate):
    def __init__(self, params):
        self.notification = list()
        bluepy.btle.DefaultDelegate.__init__(self)

    def handleNotification(self, handle, data):
        if(handle == 17):
            self.notification = struct.unpack("<BBB",data)
        else:
            return False

        return True

class Toio:
    def __init__(self, address):
        self.address = address

        try:
            self.peripheral = bluepy.btle.Peripheral()
            self.peripheral.connect(self.address, bluepy.btle.ADDR_TYPE_RANDOM)
            self.delegate = ToioDelegate(bluepy.btle.DefaultDelegate)
            self.peripheral.withDelegate(self.delegate)
        except Exception as e:
            print("Connect device failed:", e)
            sys.exit()

        self.HANDLE = Characteristic(self.peripheral)

    def button(self):
        status = {0x80 : "ON", 0x00 : "OFF"}
        ret = ""

        try:
            btn = self.peripheral.readCharacteristic(
                self.HANDLE.BUTTON_INFORMATION)
            ret = status[btn[1]]
        except Exception as e:
            print("Read Button status failed:", e)
            return False

        return ret

    def battery(self):
        try:
            bat = self.peripheral.readCharacteristic(
                self.HANDLE.BATTERY_INFORMATION)
        except Exception as e:
            print("Read Battery status failed:", e)
            return False

        return ord(bat)

    def disconnect(self):
        try:
            self.peripheral.disconnect()
        except Exception as e:
            print("Disconnect device failed:", e)
            return False

    def light_on(self, color, time = 0):
        data = [3, time, 1, 1] + color

        try:
            self.peripheral.writeCharacteristic(
                self.HANDLE.LIGHT_CONTROL,
                bytearray(data), True)
        except Exception as e:
            print("Turn on LED failed:", e)
            return False

        return True

    def light_off(self):
        try:
            self.peripheral.writeCharacteristic(
                self.HANDLE.LIGHT_CONTROL,
                bytes([1]), True)
        except Exception as e:
            print("Turn off LED failed:", e)
            return False

        return True

    def sound_effect(self, type):
        data = [2, type, 255]

        try:
            self.peripheral.writeCharacteristic(
                self.HANDLE.SOUND_CONTROL,
                bytearray(data), True)
        except Exception as e:
            print("Play Sound Effect failed", e)
            return False

        return True

    def sound(self):
        # TODO...
        pass

    def sense_position(self):
        try:
            ret = self.peripheral.readCharacteristic(
                self.HANDLE.ID_INFORMATION)
        except Exception as e:
            print("Sense Position ID failed:", e)
            return False

        # Position ID missed
        if(ret == b'\x03'):
          return False

        # use center position only
        (_, x, y, angle, _, _, _) = struct.unpack("<Bhhhhhh", ret)

        return (x, y, angle)

    def __control_motor(self, data):
        try:
            self.peripheral.writeCharacteristic(
                self.HANDLE.MOTOR_CONTROL,
                data, False)

        except Exception as e:
            print("Control motor failed:", e)
            return False

        return True

    def __control_motor_specified_time(self, param):
        if(len(param) != 7):
            print("Invalid motor parameter", param)
            return False

        data = struct.pack("<BBBBBBB", *param)

        return self.__control_motor(data)

    def __control_motor_specified_coordinate(self, param):
        if(len(param) != 10):
            print("Invalid motor parameter", param)
            return False

        data = struct.pack("<BBBBBBB"+"hhh", *param[0:7], *param[7:10])
        ret = self.__control_motor(data)

        if(ret == True):
            try:
                # request Notification
                ret = self.peripheral.writeCharacteristic(
                    self.HANDLE.MOTOR_CONTROL + 1, bytes([1]), True)

                while True:
                    if(self.peripheral.waitForNotifications(1.0)):
                        break

            except Exception as e:
                print("Receive Notification failed:", e)
                return False

            return self.delegate.notification
        else:
            return False

    def forward(self, speed = 50):
        data = [1, 1, 1, speed,2, 1, speed]
        return self.__control_motor_specified_time(data)

    def back(self, speed = 50):
        data = [1, 1, 2, speed, 2, 2, speed]
        return self.__control_motor_specified_time(data)

    def stop(self):
        data = [1, 1, 1, 0,2, 1, 0]
        return self.__control_motor_specified_time(data)

    def rotate_left(self, speed = 50):
        data = [1, 1, 2, speed, 2, 1, speed]
        ret =  self.__control_motor_specified_time(data)

        return ret

    def rotate_right(self, speed = 50):
        data = [1, 1, 1, speed, 2, 2, speed]
        ret = self.__control_motor_specified_time(data)

        return ret

    def move(self, coord_x, coord_y, angle = 0, speed = 50, move_type = 1):
        data = [3, 0, 5, move_type, speed, 0, 0, coord_x, coord_y, angle]
        ret = self.__control_motor_specified_coordinate(data)
       
        return ret

    def rotate(self, direction, angle, speed = 50):
        pos = self.sense_position()
        if(pos == False):
            return False

        if(direction == "right"):
            angle = pos[2] + angle
            if(angle > 360):
                angle = angle % 360
        else:
            angle = pos[2] - angle
            if(angle < 0):
                angle = 360 + angle 

        ret = self.move(pos[0], pos[1], angle)

        return ret

    def collision(self):
        # TODO...
        pass

    def double_tap(self):
        # TODO...
        pass

    def level(self):
        # TODO...
        pass

    def attitude(self):
        # TODO...
        pass

    def position(self):
        # TODO...
        pass

def main():
    pass

if __name__ == "__main__":
    main()
