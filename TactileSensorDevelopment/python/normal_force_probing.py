from comms_wrapper import Arduino
from loadcell_test_rig import Loadcell_test_rig
from pressure_sensor import Pressure_sensor
from utility import *
import os, json
from time import time, sleep

def main():
    # Get config information
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = json.load(open(dir_path + '/config.json'))

    # Connect sensor
    pressure_sensor = Pressure_sensor(config["sensor"]["port"], config["sensor"]["baudrate"])

    # Connect Rig
    rig = Loadcell_test_rig(config["printer"]["port"], config["printer"]["baudrate"], 
                            config["loadcell"]["port"], config["loadcell"]["baudrate"], 
                            config["printer"]["home"]["x"], config["printer"]["home"]["y"], config["printer"]["home"]["z"])


    # Query data save location and filename
    save_dir = define_csv_save_location(config["logging"]["relativeDirectory"], 
                                        config["logging"]["expSetName"])
    filename = obtain_csv_filename(save_dir)

    data_capture = {"time":[], "Fv":[], "Fh":[], "dist":[], "s1":[]}
    
    rig.begin_probing_down(zdot=config["loadcell"]["probing speed"], load_threshold=config["loadcell"]["force limit"])

    timer = time() 
    while 1:
        # Collect data
        t = time() - timer
        Fv, Fh = rig.read_loacell()
        sensor = pressure_sensor.read_sensor()
        dist = rig.zdot*(time() - rig.probe_timer)

        # Store data
        data_capture["time"].append(t)
        data_capture["Fv"].append(Fv)
        data_capture["Fh"].append(Fh)
        data_capture["dist"].append(dist)
        data_capture["s1"].append(sensor["s1"]) 
        
        # Check if probing must stop
        if rig.is_probe_limit_reached():
            break

    # Plot and save data
    plot_and_save_data(plottingData= ([data_capture["time"], data_capture["Fv"]], 
                            [data_capture["time"], data_capture["s1"]], [data_capture["dist"], data_capture["s1"]]),
                            xAxisLabel= ("Time", "Time", "Dist"), 
                            yAxisLabel =("Thrust up (g)", "Sensor", "Sensor"),
                            label = (["Loadcell up"], ["Sensor"], ["Sensor"]), 
                            savingData= (data_capture["time"], data_capture["Fv"], data_capture["Fh"], data_capture["dist"], data_capture["s1"]), 
                            filename= filename,
                            saveDir= save_dir,
                            display_plot= True, 
                            saveData = True, 
                            figsize = (6,8))

if __name__ == "__main__":
    main()