#include "pyCommsLib.h"

String msgName[] = {"s1"};
String dataCarrier[1];

float value = 0;

void setup() {
  Serial.begin(115200);
  init_python_communication();
}


void loop() {

  ///////
  // THIS IS WHERE YOU READ THE SENSOR
  //////
  value = 0;
  for(int i = 0; i<100; i++) { 
    value += analogRead(0);
  }
  value /= 100;



  dataCarrier[0] = String(value);
  
  load_msg_to_python(msgName, dataCarrier, size_of_array(msgName));
  sync(); 
}
