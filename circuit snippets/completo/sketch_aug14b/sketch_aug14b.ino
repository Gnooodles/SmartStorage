/*

  This example shows how to detect when a button or button changes the led status from off to on
  and on to off.

  The circuit:
  - pushbutton attached to pin 2 from +5V
  - 10 kilohm resistor attached to pin 2 from ground
  - LED attached from pin 13 to ground through 220 ohm resistor
*/

#include <SoftwareSerial.h>

// this constant won't change:
const int buttonPin = 7;  // the pin that the pushbutton is attached to
const int led1Pin = 8;    // the pin that the LED 1 is attached to
const int led2Pin = 4;    // the pin that te LED 2 is attached to
SoftwareSerial serio(2, 3); // RX nero, TX giallo

// Variables will change:
int led1 = 0;               // current state of the led 1
int led2 = 0;               // current state of the led 2
int buttonState = 0;        // current state of the button
int lastButtonState = 0;    // previous state of the button

int dataLength = 0;
unsigned long lastCharTime = 0;
const unsigned long timeout = 100;  // Timeout in milliseconds


void setup() {

  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the LED 1 as an output:
  pinMode(led1Pin, OUTPUT);
  // initialize the LED 2 as an output:
  pinMode(led2Pin, OUTPUT);
  // initialize serial communication:
  Serial.begin(9600);

  serio.begin(9600);
  delay(1000);
}


void loop() {

  char barcodeData[15];

  while (serio.available()) {
    char c = serio.read();
    lastCharTime = millis();  // Update last character time

    if (dataLength < sizeof(barcodeData) - 1) {
      barcodeData[dataLength++] = c;
    }
  }

  if (dataLength > 0 && millis() - lastCharTime > timeout) {
    barcodeData[dataLength] = '\0';  // Add null terminator
    Serial.println("Barcode read: " + String(barcodeData));
    dataLength = 0;
  }

  // read the pushbutton input pin:
  buttonState = digitalRead(buttonPin);

  // compare the buttonState to its previous state
  if (buttonState != lastButtonState) {
    // if the state has changed, increment the counter
    if (buttonState == HIGH) {
      // if the state has changed (the botton is pressed), change the led status (on or off)
      if (led1 == 0){
        led1 = 1; // led1 status on
        led2 = 0; // led2 status off
        Serial.println("CARICA");
      } else {
        led1 = 0; // led1 status off
        led2 = 1; // led2 status on
        Serial.println("SCARICA");
      }
    }
    // Delay a little bit to avoid bouncing
    delay(50);
  }
  // save the current state as the last state, for next time through the loop
  lastButtonState = buttonState;

  // if the led 1 status is on set the led on HIGH else on LOW 
  if (led1 == 1){
    digitalWrite(led1Pin, HIGH);
  } else {
    digitalWrite(led1Pin, LOW);
  }
  
  // if the led 2 status is on set the led on HIGH else on LOW 
  if (led2 == 1){
    digitalWrite(led2Pin, HIGH);
  } else {
    digitalWrite(led2Pin, LOW);
  }

}