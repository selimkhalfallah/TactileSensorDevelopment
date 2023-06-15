#include "pyCommsLib.h"

// Define number of sensor readings here
// If you have 2 sensor for example, do 
// String msgName[] = {"s1", "s2"}; String dataCarrier[2];

String msgName[] = {"s1"};
String dataCarrier[1];


void setup() {
  Serial.begin(115200);
  
  // Initialize python-arduino communication
  init_python_communication();
}


void loop() {

  // Read sensor values here

  dataCarrier[0] = "You_sensor_value_as_a_string";
  
  load_msg_to_python(msgName, dataCarrier, size_of_array(msgName));
  sync(); 
}
