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

int actdelay = 10; //number of loops for the activation of a pin, each loop lasts between 5 and 10ms
int Sig1On = 0;
int Sig2On = 0;

SX1262 radio = new Module(CS, DIO1, RESET, BUSY);

void setup() {
  Serial.begin(9600);
  bool fail = false;
  // initialize SX1262 with default settings
  do{
    Serial.print(F("Initializing ... "));
    int state = radio.begin(freq);
    if (state == RADIOLIB_ERR_NONE) {
      Serial.println(F("success!"));
      fail = false;
    } else {
      Serial.print(F("failed, code "));
      Serial.println(state);
      Serial.println("trying again...");
      fail = true;
    }
  }
  while (fail);  

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
      if (Sig1On == 0){
        digitalWrite(SIG1, HIGH);
        Sig1On += 1;
      }
    }else if (str == "SIG2"){
      if (Sig2On == 0){
        digitalWrite(SIG2, HIGH);
        Sig2On += 1;
      }
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
  if (Sig1On > 0){
    if Sig1On = actdelay{
      digitalWrite(SIG1, LOW);
    }else{
      Sig1On += 1;
    }
  }
  if (Sig2On > 0){
    if Sig2On = actdelay{
      digitalWrite(SIG2, LOW);
    }else{
      Sig2On += 1;
    }
  }
}
