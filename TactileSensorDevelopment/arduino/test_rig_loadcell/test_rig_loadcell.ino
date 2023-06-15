#include "pyCommsLib.h"
#include "HX711.h"

String msgName[] = {"status", "lc up", "lc side"};
String dataCarrier[3];

// LOAD CELL
HX711 loadcell_up;
HX711 loadcell_side;

uint8_t dataPin_up = 2;
uint8_t clockPin_up = 3;

uint8_t dataPin_side = 4;
uint8_t clockPin_side = 5;

volatile float load_up;
volatile float load_side;
 

// MISC
String operation_mode = "";
long timer;

void setup() {
  Serial.begin(115200);

  // Initialize the load cell
  loadcell_up.begin(dataPin_up, clockPin_up);
  loadcell_up.set_scale(3070);
  loadcell_up.tare(); 

  // Initialize the load cell
  loadcell_side.begin(dataPin_side, clockPin_side);
  loadcell_side.set_scale(3050);
  loadcell_side.tare(); 

  
  // Initialize python-arduino communication
  init_python_communication();
}


void loop() {
  // Get operation mode from python side
  operation_mode = latest_received_msg();

  if(operation_mode == "reset") { 
    // reset stuff here
    loadcell_up.tare();
    loadcell_side.tare();
  }
  
  dataCarrier[0] = "steady";
  dataCarrier[1] = String(loadcell_up.get_units());
  dataCarrier[2] = String(loadcell_side.get_units());

  load_msg_to_python(msgName, dataCarrier, size_of_array(msgName));
  sync(); 
}
