from printer_comms import Printer
from comms_wrapper import Arduino
from utility import *

from time import time, sleep

class Loadcell_test_rig(Printer):
    
    def __init__(self, printer_port, printer_baudrate, loadcell_port, loadcell_baudrate,
                        home_x, home_y, home_z):
        super().__init__("Printer", printer_port, printer_baudrate)

        self.home_x = home_x
        self.home_y = home_y
        self.home_z = home_z

        # Connect to printer
        self.connect()

        # Connect to loadcells
        self.loadcell = Arduino("loadcell", loadcell_port, loadcell_baudrate)
        self.loadcell.connect_and_handshake()

        self.reset_loadcell()

        self.setup_and_datum()

    def setup_and_datum(self):
        print("\nWait until the probe moves to the defined home pos\n")
        self.move_datum()
        self.set_home_pos(self.home_x, self.home_y, self.home_z)
        self.send_gcode("M203 Z20", printMsg=False)
        self.move_axis(z=0)
        self.move_home()

    def reset_loadcell(self):
        print("\nResetting loadcell\n")
        
        self.loadcell.send_message(["reset"])
        sleep(1.5)
        self.loadcell.send_message(["sensing"])
        
    def read_loacell(self):
        self.loadcell.receive_message()
        msg = self.loadcell.receivedMessages

        lc_vertical = float(msg["lc up"])
        lc_horizontal = float(msg["lc side"])

        return lc_vertical, lc_horizontal
    
    def move_z_to_home(self):
        self.move_axis_absolute(z = self.home_z)
    
    def move_xy(self, x, y, speed = 4000):
        self.move_axis(x=x, y=y, f=speed)

    def begin_probing_down(self, zdot, load_threshold):
        self.zdot = zdot
        self.load_threshold = load_threshold
        
        self.z_start = self.read_position(printMsg=False)[2]
        self.probe_timer = time()
        self.move_z_speed(zdot)
        
    def is_probe_limit_reached(self):
        curr_z = round(self.z_start - self.zdot*(time() - self.probe_timer))

        F_v, _ = self.read_loacell()

        if curr_z < 0 or F_v > self.load_threshold or F_v > 450:
            self.abort_motion()

            self.send_gcode("M203 Z20", printMsg=False)
            self.move_axis_absolute(z = curr_z + 30)

            self.move_z_to_home()

            return True
    
        else:
            return False