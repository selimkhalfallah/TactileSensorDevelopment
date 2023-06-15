import serial
from threading import Thread
from time import time, sleep
import sys

class Printer:
    def __init__(self, descriptive_device_name, port_name, baudrate):
        # Communication inputs
        self.descriptive_device_name = descriptive_device_name
        self.port_name = port_name
        self.baudrate = baudrate

        # Communication
        self._raw_received_message = None
        self.printer = None
        self._ok_flag = False

        # Other
        self.home_pos = [0,0,0]

    def _serial_readline(self):
        while 1:
            try:
                self._raw_received_message = self.printer.readline().decode('utf-8')[:-1]
                if self._raw_received_message == "ok":
                    self._ok_flag = True
            except:
                pass
            sleep(0.001)

    def _start_Reading_Thread(self):
        self.__thread = Thread(target=self._serial_readline)
        self.__thread.daemon = True
        self.__thread.start()

    def connect(self, timeout = 20):
        try: 
            self.printer = serial.Serial(port=self.port_name, baudrate=self.baudrate)
            print("Successfully connected to " + self.descriptive_device_name)
        except:
            print("!! Cannot connect to " + self.descriptive_device_name + " !!")
            sys.exit()

        self._start_Reading_Thread()

        print("Waiting until pritner initializes")
        timer = time()
        while True:
            if self._raw_received_message == "echo:SD init fail":
                print("Successfully initialized " + self.descriptive_device_name)
                break

            if time() - timer > timeout:
                print("!! " +  self.descriptive_device_name + " init failed !!")
                sys.exit()

    def disconnect(self):
        try: 
            self.printer.close()
            print("Disconnected " + self.descriptive_device_name)
        except:
            print("!! Cannot disconnect " + self.descriptive_device_name + " !!")
            sys.exit()

    def _send_msg(self, msg):
        self.printer.write(str.encode(msg)) 

    def send_gcode(self, gcode, wait_until_completion = True, printMsg = True):
        self._ok_flag = False
        self._send_msg(gcode + "\r\n")

        if wait_until_completion:
            while True:
                if self._ok_flag: 
                    break
            if printMsg:
                print("Process complete: ", gcode)

    def move_z_speed(self, speed):
        self.send_gcode("M203 Z" + str(float(speed)), printMsg=False)
        self.move_axis_absolute(z = 0)

    def abort_motion(self):
        print("Stopping steppers...")
        self.send_gcode("M410", printMsg=False)
        print("Steppers back in service")

    def set_home_pos(self, x, y, z):
        self.home_pos = [x, y, z]

    def move_datum(self, printMsg=False):
        self.send_gcode("G28 X0 Y0 Z0", printMsg=printMsg)

    def move_home(self, feedrate = 3000, printMsg=False):
        self.move_axis_absolute(x = self.home_pos[0], 
                                y = self.home_pos[1], 
                                z = self.home_pos[2], 
                                f = feedrate,
                                printMsg=printMsg)

    def move_axis(self, x = None, y = None, z = None, f = None, printMsg = False):
        command = "G0"
        if x is not None:
            command = command + " X" + str(x + self.home_pos[0])
        if y is not None:
            command = command + " Y" + str(y + self.home_pos[1])
        if z is not None:
            command = command + " Z" + str(z + self.home_pos[2])
        if f is not None:
            command = command + " F" + str(f)
        else:
            command = command + " F1500"

        self.send_gcode(command, wait_until_completion=True, printMsg=printMsg)

    def move_axis_absolute(self, x = None, y = None, z = None, f = None, printMsg = False):
        command = "G0"
        if x is not None:
            command = command + " X" + str(x)
        if y is not None:
            command = command + " Y" + str(y)
        if z is not None:
            command = command + " Z" + str(z)
        if f is not None:
            command = command + " F" + str(f)
        else:
            command = command + " F1500"

        self.send_gcode(command, wait_until_completion=True, printMsg=printMsg)

    def read_position(self, printMsg=True):
        self.send_gcode("M114", wait_until_completion=False, printMsg=printMsg)

        pos = None
        while True:
            if self._raw_received_message[:1] == "X" and pos is None:
                pos = self._raw_received_message

            if self._ok_flag and (pos is not None): 
                break
        
        if printMsg:
            print("position:", pos)

        msg = pos.split(":")
        position = []
        for i, m in enumerate(msg):
            if i > 0 and i < 4:
                position.append(float(m[:-2]))

        return position