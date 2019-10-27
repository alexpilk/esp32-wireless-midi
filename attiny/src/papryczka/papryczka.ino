#include <SoftwareSerial.h>  //Software Serial Port
#define RxD 1
#define TxD 2

#define DEBUG_ENABLED  1

SoftwareSerial blueToothSerial(RxD, TxD);

int led = 4;
const int buttonPin = 3;

void setup()
{
  pinMode(RxD, INPUT);
  pinMode(TxD, OUTPUT);
  setupBlueToothConnection();

  pinMode(led, OUTPUT);
  pinMode(buttonPin, INPUT);
  digitalWrite(led, HIGH);

}

String cache = "";
void loop(){
  int count = 0;
//  char recvChar;
  while (1) {
//    blueToothSerial.print("AT\n\r" + cache);
    delay(100);
//    delay(3000);
    //check if there's any data sent from the remote bluetooth shield
    if (blueToothSerial.available()) {
      String recvChar = blueToothSerial.readString();
      blueToothSerial.print(recvChar+"o");
//      recvChar = blueToothSerial.read();
//      blueToothSerial.print(recvChar);
      count++ ;
      if (count % 2 == 0)
        digitalWrite(led, HIGH);

      else
        digitalWrite(led, LOW);
    }
//    delay(1000);
    int buttonState = digitalRead(buttonPin);
    if(buttonState == HIGH) {
        digitalWrite(led, LOW);
      blueToothSerial.print("pressed!");
      
    }
//      blueToothSerial.print("\r\n");
  }
  
}
void write(String command){
    blueToothSerial.print("\r\nAT+" + command + "\r\n"); //set the bluetooth name as "HC-05"
    blueToothSerial.readString();
    delay(1000);
  
}
void setupBlueToothConnection()
{
  blueToothSerial.begin(9600); //Set BluetoothBee BaudRate to default baud rate 38400
//    blueToothSerial.print("\r\n+STWMOD=0\r\n"); //set the bluetooth work in slave mode
//    blueToothSerial.print("\r\n+NAMEdupiuhakius\r\n"); //set the bluetooth name as "HC-05"
    write("NAMEpapryczka");
    write("ROLE0");
    write("IMME0");
    write("RESET");
    write("NOTI1");
//    blueToothSerial.print("\r\n+STOAUT=1\r\n"); // Permit Paired device to connect me
//    blueToothSerial.print("\r\n+STAUTO=0\r\n"); // Auto-connection should be forbidden hereAT+PIN008888
//    blueToothSerial.print("\r\nAT+TYPE1\r\n"); // Auto-connection should be forbidden here
//    blueToothSerial.print("\r\nAT+PASS008888\r\n"); // Auto-connection should be forbidden here
blueToothSerial.print("\r\nAT+ADDR?\r\n");
delay(200);
    cache = blueToothSerial.readString();
  delay(2000); // This delay is required.
//  blueToothSerial.print("\r\n+INQ=1\r\n"); //make the slave bluetooth inquirable
  blueToothSerial.print("bluetooth connected!\n");

  delay(2000); // This delay is required.
  blueToothSerial.flush();
}
