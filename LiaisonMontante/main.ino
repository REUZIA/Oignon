// include the library
#include <RadioLib.h>

//Connections :
//SX   | NAME | PIN -> ARDUINO PIN
//BUSY | PB1  | 13  -> 9
//CS   | PB2  | 14  -> 10
//MOSI | PB3  | 15  -> 11
//MISO | PB4  | 16  -> 12
//CLK  | PB5  | 17  -> 13
//DIO1 | PD2  | 32  -> 2
//RESET| PD3  | 1   -> 3
//SIG1 | PC2  | 25  -> 16/A2
//SIG2 | PC4  | 27  -> 18/A4
int CS = 10;
int DIO1 = 2;
int RESET = 3;
int BUSY = 9;
int SIG1 = 16;
int SIG2 = 18;

int freq = 863.75;

SX1262 radio = new Module(CS, DIO1, RESET, BUSY);

void setup() {
  Serial.begin(9600);

  // initialize SX1262 with default settings
  Serial.print(F("Initializing ... "));
  int state = radio.begin(freq);
  if (state == RADIOLIB_ERR_NONE) {
    Serial.println(F("success!"));
  } else {
    Serial.print(F("failed, code "));
    Serial.println(state);
    while (true) { delay(10); }
  }

  pinMode(SIG1, OUTPUT);
  pinMode(SIG2, OUTPUT);
}

void loop() {
  Serial.print(F("Waiting for incoming transmission ... "));

  // you can receive data as an Arduino String
  String str;
  int state = radio.receive(str);

  if (state == RADIOLIB_ERR_NONE) {
    // packet was successfully received
    Serial.println(F("success!"));

    // print the data of the packet
    Serial.print(F("Data:\t\t"));
    Serial.println(str);

    if (str == "SIG1"){
      digitalWrite(SIG1, HIGH);
    }else if (st == "SIG2"){
      digitalWrite(SIG2, HIGH);
    }
  } else if (state == RADIOLIB_ERR_RX_TIMEOUT) {
    // timeout occurred while waiting for a packet
    Serial.println(F("timeout!"));

  } else if (state == RADIOLIB_ERR_CRC_MISMATCH) {
    // packet was received, but is malformed
    Serial.println(F("CRC error!"));

  } else {
    // some other error occurred
    Serial.print(F("failed, code "));
    Serial.println(state);

  }
}