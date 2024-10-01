
from sx1262 import SX1262
import time

def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print(msg)
        print(error)

sx = SX1262(spi_bus=0, clk=18, mosi=19, miso=16, cs=27, irq=20, rst=15, gpio=26)

# LoRa
sx.begin(freq=863.75, bw=500, sf=12, cr=8, syncWord=0x34,
         power=14, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

# FSK
##sx.beginFSK(freq=923, br=48.0, freqDev=50.0, rxBw=156.2, power=-5, currentLimit=60.0,
##            preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
##            addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
##            crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
##            fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
##            tcxoVoltage=1.6, useRegulatorLDO=False,
##            blocking=True)

sx.setBlockingCallback(False, cb)


from machine import Pin

# Configurer GP0 en mode pull-down
gp0 = Pin(0, Pin.IN, Pin.PULL_DOWN)

# Configurer GP14 en mode pull-down
gp14 = Pin(14, Pin.IN, Pin.PULL_DOWN)

print("att")
while True:
    # Lire l'état des broches GP0 et GP14
    gp0_state = gp0.value()
    gp14_state = gp14.value()

    # if gp0_state or gp14_state:

    # Afficher l'état des broches sur la console
    print(f"GP0: {gp0_state}, GP14: {gp14_state}")
    
    sx.send(b'SIG1')
    
    # Attendre un peu avant de lire à nouveau
    time.sleep(1)
