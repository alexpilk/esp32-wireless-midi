#include "Arduino.h"
#include "Button.h"

Button::Button(int pin)
{
  pinMode(pin, INPUT);
  this->_pin = pin;
}

bool Button::check(SoftwareSerial bt)
{
  int reading = digitalRead(this->_pin);

  if (reading == this->_lastButtonState) {
    return false;
  }

  bool isNoise = ((millis() - this->_lastDebounceTime) < this->_debounceDelay);

  this->_lastDebounceTime = millis();
  this->_lastButtonState = reading;

  bool buttonPressed = !isNoise && reading == HIGH;

  return buttonPressed;
}