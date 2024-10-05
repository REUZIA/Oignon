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
int SIG1 = A2;
int SIG2 = A4;

int actdelay = 10000; //number of loops for the activation of a pin
int Sig1On = 0;
int Sig2On = 0;

SX1262 radio = new Module(CS, DIO1, RESET, BUSY);

void setup() {
  Serial.begin(9600);
  bool fail = false;
  // initialize SX1262 with default settings
  do{
    Serial.print(F("Initializing ... "));
    // carrier frequency:           863.75
    // bandwidth:                   500.0 kHz
    // spreading factor:            12
    // coding rate:                 8
    // sync word:                   0x34 (public network/LoRaWAN)
    // output power:                14 dBm
    // preamble length:             20 symbols
    int state = radio.begin(863.75, 500.0, 12, 8, 0x34, 14, 8);
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

  // set the function that will be called
  // when new packet is received
  radio.setPacketReceivedAction(setFlag);

  // start listening for LoRa packets
  do{
    Serial.print(F("Starting to listen ... "));
    int state = radio.startReceive();
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
}

// flag to indicate that a packet was received
volatile bool receivedFlag = false;

// this function is called when a complete packet
// is received by the module
// IMPORTANT: this function MUST be 'void' type
//            and MUST NOT have any arguments!
void setFlag(void) {
  // we got a packet, set the flag
  receivedFlag = true;
}


void loop() {
  // check if the flag is set
  if(receivedFlag) {
    // reset flag
    receivedFlag = false;
    
    // you can read received data as an Arduino String
    String str;
    int state = radio.readData(str);

    if (state == RADIOLIB_ERR_NONE) {
      // packet was successfully received
      Serial.println(F("Received packet!"));

      // print data of the packet
      Serial.print(F("Data:\t\t"));
      Serial.println(str);

      if (str == "SIG1"){
        Serial.println("SIG1 received");
        if (Sig1On == 0){
          digitalWrite(SIG1, HIGH);
          Sig1On += 1;
        }
      }
      if (str == "SIG2"){
        Serial.println("SIG2 received");
        if (Sig2On == 0){
          digitalWrite(SIG2, HIGH);
          Sig2On += 1;
          }
      }
      
  } else if (state == RADIOLIB_ERR_CRC_MISMATCH) {
      // packet was received, but is malformed
      Serial.println(F("CRC error!"));

  } else {
    // some other error occurred
    Serial.print(F("failed, code "));
    Serial.println(state);
  }
 }
 if (Sig1On > 0){
  if (Sig1On >= actdelay){
  digitalWrite(SIG1, LOW);
      Sig1On = 0;
    }else{
      Sig1On += 1;
    }
  }
  if (Sig2On > 0){
    if (Sig2On >= actdelay){
      digitalWrite(SIG2, LOW);
      Sig2On = 0;
    }else{
      Sig2On += 1;
    }
  }
}
