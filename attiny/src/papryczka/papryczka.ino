#include <SoftwareSerial.h>  //Software Serial Port
#include <Button.h>

#define RxD 1
#define TxD 2

#define DEBUG_ENABLED  1

SoftwareSerial blueToothSerial(RxD, TxD);

const int led = 4;
const int buttonPin = 3;
int lastLed = HIGH;

Button button1(3);
Button button2(0);

void setup()
{
  setPinModes();
  setupBlueToothConnection();
//  button = Button(3);
  digitalWrite(led, HIGH);
}

void setPinModes() {
  pinMode(RxD, INPUT);
  pinMode(TxD, OUTPUT);
  pinMode(led, OUTPUT);
  pinMode(buttonPin, INPUT);
}

void loop() {
  int count = 0;
  while (1) {
    delay(100);
    if (blueToothSerial.available()) {
      String recvChar = blueToothSerial.readString();
      blueToothSerial.flush();
//      blueToothSerial.print(recvChar + "o");
      count++ ;
      if (count % 2 == 0)
        digitalWrite(led, HIGH);
      else
        digitalWrite(led, LOW);
    }
    if(button1.check()) {
      
        blueToothSerial.print("0");
        digitalWrite(led, lastLed);
    }
    if(button2.check()) {
      
        blueToothSerial.print("1");
        digitalWrite(led, lastLed);
    }
//    checkButtons(3, "0");
//    checkButtons(0, "1");
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
  delay(2000); // This delay is required.
  blueToothSerial.print("bluetooth connected!\n");

  delay(2000); // This delay is required.
  blueToothSerial.flush();
}
