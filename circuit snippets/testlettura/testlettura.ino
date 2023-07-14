#include <SoftwareSerial.h>

SoftwareSerial ss(2, 3); // RX, TX


void setup() {
  Serial.begin(9600);
  ss.begin(9600);
  delay(1000);
  Serial.println("pronto");
}


void loop() {
  if (ss.available() > 0) {
    Serial.write(ss.read()); 
    Serial.println("Ho scansionato");
  }
}
