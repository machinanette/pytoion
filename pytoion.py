import bluepy
import time
import struct
from define import LedColor, SoundEffect, Characteristic

class ToioDelegate(bluepy.btle.DefaultDelegate):
    def __init__(self, params):
        self.notification = dict()
        bluepy.btle.DefaultDelegate.__init__(self)

    def handleNotification(self, handle, data):
        self.handle = handle
        if(handle == self.HANDLE.MOTOR_CONTROL):
            self.notification["motor"] = struct.unpack("<BBB",data)
        elif(handle == self.HANDLE.BUTTON_INFORMATION):
            self.notification["button"] = data[1]
        elif(handle == self.HANDLE.SENSOR_INFORMATION):
            self.notification["motion"] = struct.unpack("<BBBBB",data)
        return True

class Toio:
    def __init__(self, address):
        self.address = address

        self.COLOR = LedColor()
        self.SE = SoundEffect()

        try:
            self.peripheral = bluepy.btle.Peripheral()
            self.peripheral.connect(self.address, bluepy.btle.ADDR_TYPE_RANDOM)
        except Exception as e:
            print("Connect device failed:", e)
            sys.exit()

        try:
            handle = Characteristic()
            charas = self.peripheral.getCharacteristics()
            handle_dic = handle._asdict()
            del(handle_dic["UUID_DIC"])

            for chara in charas:
                key = str(chara.uuid).split("-")[0]
                if(key in handle.UUID_DIC):
                    handle_dic[handle.UUID_DIC[key]] = chara.getHandle()

            self.HANDLE = Characteristic(**handle_dic)
        except Exception as e:
            print("Get Handle id Failed:", e)
            sys.exit()

        try:
            self.delegate = ToioDelegate(bluepy.btle.DefaultDelegate)
            self.peripheral.withDelegate(self.delegate)
            self.delegate.HANDLE = self.HANDLE
        except Exception as e:
            print("Set delegate failed:", e)
            sys.exit()

        try:
            notification = [
                self.HANDLE.MOTOR_CONTROL,
                self.HANDLE.BUTTON_INFORMATION,
                self.HANDLE.SENSOR_INFORMATION
            ]

            for i in notification:
                self.peripheral.writeCharacteristic(
                    i + 1, bytes([1]), True)
                
        except:
            print("Set notification failed:", e)
            sys.exit()

    def button(self):
        status = {0x80 : "PUSH", 0x00 : "RELEASE"}

        try:
            while True:
                if(self.peripheral.waitForNotifications(1.0)):
                    break
        except Exception as e:
            print("Read Button status failed:", e)
            return False

        return  status[self.delegate.notification["button"]]

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

    def led_on(self, color, time = 0):
        data = tuple([3, time, 1, 1]) + color

        try:
            self.peripheral.writeCharacteristic(
                self.HANDLE.LIGHT_CONTROL,
                bytearray(data), True)
        except Exception as e:
            print("Turn on LED failed:", e)
            return False

        return True

    def led_off(self):
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

    def sense_motion(self):
        try:
            while True:
                if(self.peripheral.waitForNotifications(1.0) and
                   self.delegate.handle == self.HANDLE.SENSOR_INFORMATION):
                    break

        except Exception as e:
            print("Receive Notification failed:", e)
            return False

        return self.delegate.notification["motion"]

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

        if ret:
            try:
                while True:
                    if(self.peripheral.waitForNotifications(1.0) and
                       self.delegate.handle == self.HANDLE.MOTOR_CONTROL):
                        break

            except Exception as e:
                print("Receive Notification failed:", e)
                return False

            return self.delegate.notification["motor"]
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
