# Pritner Loadcell Test Rig


<img src="/Images/overview.jpg" alt="Overview" width="400"/>
<img src="/Images/lc_closeup.jpg" alt="Overview" width="300"/>
<img src="/Images/lc_faraway.jpg" alt="Overview" width="300"/>

## Overview
Force measurement tool for indentation motion device using a 3D printer rig. This device can be used for testing a variety of things. For example:
- Force-displacement characteristics of a soft object
- Indentation test to obtain the resolution/sensitivity of a sensor with ground truth displacement and force readings in two axis (normal and one sheer)

## Functionality
### Hardware functionality
- Cartesian xyz rig from an FDM 3D printer (Anycubic Mega Zero)
- Two load cells (500g max) mountd on the nozzle location, each measuring orthogonal directions
- Arduino Uno to continously read the load cell values

### Software functionality
- `config.json`: Config file to store port names (e.g.: "COM3", "/dev/ttyACM0") and baudrates, file save locations
- `python/normal_force_probing.py`: Sample code to use the rig for normal force probing
- `python/loadcell_test_rig.py`: Abstraction class to use the printer + loadcell arduino
- `python/printer_comms.py`: Abstraction class to use the printer without sending individual gcode commands
- `python/comms_wrapper.py`: Abstraction class for bidirectional communication with Arduinos
- `python/utility.py`: Python functions which are of general utility, e.g.: plotting, file i/o, etc
- `arduino/test_rig_loadcell`: Contains code uploaded to the arduino reading the loadcells
- `arduino/your_sensor_arduino`: Contains sample code which you can use to read your sensor values
