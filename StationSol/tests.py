from lib.sx1262 import SX1262
import sys
import time

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

lastpck = 0

def cbRX(events): #callback function when RX event occurs
    if events & SX1262.RX_DONE: #we make sure the transmission is done before reading it
	global lastpck
        msg, err = sxRX.recv()
        error = SX1262.STATUS[err]
        print(msg)
        print(error)
	print(sxRX.getRSSI())
	rxpck = time.ticks_ms()
	print(time.ticks_diff(rxpck, lastpck))
	lastpck = rxpck
def cbTX(events): #callback function when TX event occurs
    if events & SX1262.TX_DONE:
        print('TX done.')

def test1():
	sxRX.begin(freqRX, bw=500.0, sf=12, cr=8, syncWord=0x34,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
	sxTX.begin(freqTX, bw=500.0, sf=12, cr=8, syncWord=0x34,
		 power=14, currentLimit=60.0, preambleLength=8,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

	sxRX.setBlockingCallback(False, cbRX)
	sxTX.setBlockingCallback(False, cbTX)
	sxTX.send(b"SIG1")
	time.sleep(1)
	sxTX.send(b"SIG1")
	time.sleep(1)
	sxTX.send(b"SIG1")
	time.sleep(1)
	sxTX.send(b"SIG2")
	time.sleep(1)
	sxTX.send(b"SIG2")
	time.sleep(1)
	sxTX.send(b"SIG2")
	time.sleep(1)

def test2():
	sxRX.begin(freqRX, bw=250.0, sf=12, cr=8, syncWord=0x34,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

	sxRX.setBlockingCallback(False, cbRX)


def test3():
	sxRX.begin(freqRX, bw=125.0, sf=12, cr=8, syncWord=0x34,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

	sxRX.setBlockingCallback(False, cbRX)

def test4():
	sxRX.begin(freqRX, bw=500.0, sf=9, cr=8, syncWord=0x34,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

	sxRX.setBlockingCallback(False, cbRX)

def test5():
	sxRX.begin(freqRX, bw=500.0, sf=7, cr=8, syncWord=0x34,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

	sxRX.setBlockingCallback(False, cbRX)

def test6():
	sxRX.begin(freqRX, bw=500.0, sf=12, cr=6, syncWord=0x34,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

	sxRX.setBlockingCallback(False, cbRX)

def test7():
	sxRX.begin(freqRX, bw=500.0, sf=12, cr=5, syncWord=0x34,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

	sxRX.setBlockingCallback(False, cbRX)

def test8_9():
	sxRX.begin(freqRX, bw=500.0, sf=12, cr=8, syncWord=0x34,
		 implicit=False, implicitLen=0xFF,
		 crcOn=True, txIq=False, rxIq=False,
		 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

	sxRX.setBlockingCallback(False, cbRX)
