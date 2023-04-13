/*

  This example shows how to detect when a button or button changes the led status from off to on
  and on to off.

  The circuit:
  - pushbutton attached to pin 2 from +5V
  - 10 kilohm resistor attached to pin 2 from ground
  - LED attached from pin 13 to ground through 220 ohm resistor
*/

// this constant won't change:
const int buttonPin = 2;  // the pin that the pushbutton is attached to
const int ledPin = 8;    // the pin that the LED is attached to

// Variables will change:
int ledOn = 0;              // current state of the led
int buttonState = 0;        // current state of the button
int lastButtonState = 0;    // previous state of the button

void setup() {

  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the LED as an output:
  pinMode(ledPin, OUTPUT);
  // initialize serial communication:
  Serial.begin(9600);
}


void loop() {

  // read the pushbutton input pin:
  buttonState = digitalRead(buttonPin);

  // compare the buttonState to its previous state
  if (buttonState != lastButtonState) {
    // if the state has changed, increment the counter
    if (buttonState == HIGH) {
      // if the state has changed (the botton is pressed), change the led status (on or off)
      if (ledOn == 0){
        ledOn = 1; // led status on
      } else {
        ledOn = 0; // led status off
      }
    }
    // Delay a little bit to avoid bouncing
    delay(50);
  }
  // save the current state as the last state, for next time through the loop
  lastButtonState = buttonState;

  // if the led status is on set the led on HIGH else on LOW 
  if (ledOn == 1){
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
}
