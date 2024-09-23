from lib.sx1262 import SX1262
import time
import threading
import uselect
import sys

def cbRX(events):
    if events & SX1262.RX_DONE:
        msg, err = sxRX.recv()
        error = SX1262.STATUS[err]
        print(msg)
        print(error)
def cbTX(events):
    if events & SX1262.TX_DONE:
        print('TX done.')

sxRX = SX1262(spi_bus=1, clk=26, mosi=27, miso=28, cs=19, irq=20, rst=15, gpio=6)
sxTX = SX1262(spi_bus=0, clk=2, mosi=3, miso=4, cs=11, irq=12, rst=7, gpio=10)

sxRX.begin(freq=869.75, bw=500.0, sf=12, cr=8, syncWord=0x34,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
sxTX.begin(freq=863.75, bw=500.0, sf=12, cr=8, syncWord=0x34,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

sxRX.setBlockingCallback(False, cbRX)
sxTX.setBlockingCallback(False, cbTX)

spoll=uselect.poll()
spoll.register(sys.stdin,uselect.POLLIN)
def read1():
    return(sys.stdin.read(1) if spoll.poll(0) else None)

# main loop
while True:
    c = read1()
    if c != None:
        sxTX.send(c)
        pass