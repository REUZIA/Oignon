from lib.sx1262 import SX1262
import time
import threading
import uselect
import sys

#Connections :
#SX   |     PIN -> GPIO
#MOD  |	MODULE 1 | MODULE 2	
#BUS  | BUS 1	 | BUS 0	
#CLK  | 38 -> 26 | 3  -> 2	
#MOSI | 39 -> 27 | 5  -> 3	
#MISO | 40 -> 28 | 6  -> 4
#CS   | 30 -> 19 | 14 -> 11
#DIO1 | 31 -> 20 | 15 -> 12
#RESET| 12 -> 15 | 9  -> 7
#BUSY | 8  -> 6  | 13 -> 10
sxRX = SX1262(spi_bus=1, clk=26, mosi=27, miso=28, cs=19, irq=20, rst=15, gpio=6)
sxTX = SX1262(spi_bus=0, clk=2, mosi=3, miso=4, cs=11, irq=12, rst=7, gpio=10)

freqRX = 869.75
freqTX = 863.75

def cbRX(events): #callback function when RX event occurs
    if events & SX1262.RX_DONE: #we make sure the transmission is done before reading it
        msg, err = sxRX.recv()
        error = SX1262.STATUS[err]
        print(msg)
        print(error)
def cbTX(events): #callback function when TX event occurs
    if events & SX1262.TX_DONE:
        print('TX done.')
def read1():
    return(sys.stdin.read(1) if spoll.poll(0) else None)

sxRX.begin(freqRX, bw=500.0, sf=12, cr=8, syncWord=0x34,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
sxTX.begin(freqTX, bw=500.0, sf=12, cr=8, syncWord=0x34,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

sxRX.setBlockingCallback(False, cbRX)
sxTX.setBlockingCallback(False, cbTX)

spoll=uselect.poll()
spoll.register(sys.stdin,uselect.POLLIN)

send_data = ""
send_char = "#" #char used to end line and send data

# main loop
while True:
    c = read1()
    if c != None:
        if c == send_char:
            sxTX.send(send_data)
            send_data = ""
            pass
        else:
            send_data = send_data + c
