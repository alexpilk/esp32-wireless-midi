#include <SoftwareSerial.h>  //Software Serial Port
#define RxD 1
#define TxD 2

#define DEBUG_ENABLED  1

SoftwareSerial blueToothSerial(RxD, TxD);

const int led = 4;
const int buttonPin = 3;

void setup()
{
  setPinModes();
  setupBlueToothConnection();
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
      blueToothSerial.print(recvChar + "o");
      count++ ;
      if (count % 2 == 0)
        digitalWrite(led, HIGH);
      else
        digitalWrite(led, LOW);
    }
    checkButtons();
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
