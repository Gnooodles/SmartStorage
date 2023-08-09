#include <SoftwareSerial.h>

SoftwareSerial serio(3, 2); // RX nero, TX giallo


void setup() {
  Serial.begin(9600);
  serio.begin(9600);
  delay(1000);
}


void loop() {
  if (serio.available() > 0) {
    Serial.write(serio.read());
  }
}
