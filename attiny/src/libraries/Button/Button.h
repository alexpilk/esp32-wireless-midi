/*
  Morse.h - Library for flashing Morse code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/
#ifndef Morse_h
#define Morse_h

#include "Arduino.h"
#include <SoftwareSerial.h>
class Button
{
  public:
    Button(int pin);
    bool check(SoftwareSerial bt);
  private:
    int _pin;
    int _buttonState;
    int _lastButtonState;// the previous reading from the input pin
    unsigned long _lastDebounceTime = 0;  // the last time the output pin was toggled
    unsigned long _debounceDelay = 10;    // the debounce time; increase if the output flickers
};

#endif