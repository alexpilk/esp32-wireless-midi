#include <SoftwareSerial.h>  //Software Serial Port
#include <Button.h>

#define RxD 1
#define TxD 2

#define DEBUG_ENABLED  1

SoftwareSerial blueToothSerial(RxD, TxD);

Button buttons[] = {Button(3), Button(0), Button(4)};

void setup()
{
  setPinModes();
  setupBlueToothConnection();
}

void setPinModes() {
  pinMode(RxD, INPUT);
  pinMode(TxD, OUTPUT);
}

void loop() {
  for (int i = 0; i < 3; i++) {
    checkButton(&buttons[i], i);
  }
}

void checkButton(Button* button, int message) {
    if(button->check(blueToothSerial)) { 
        blueToothSerial.print(message);
    }
}

void write(String command) {
  blueToothSerial.print("\r\nAT+" + command + "\r\n");
  blueToothSerial.readString();
  delay(500);

}
void setupBlueToothConnection()
{
  blueToothSerial.begin(9600);
  write("DEFAULT");
  write("RESET");
  write("NAMEpapryczka");
  write("ROLE0");
  write("IMME0");
  write("RESET");
  write("NOTI1");
  blueToothSerial.flush();
}
