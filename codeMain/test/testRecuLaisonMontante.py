
from sx1262 import SX1262
import time

# def cb(events):
#     if events & SX1262.RX_DONE:
#         msg, err = sx.recv()
#         error = SX1262.STATUS[err]
#         print(msg)
#         print(error)

# sx = SX1262(spi_bus=0, clk=2, mosi=3, miso=4, cs=27, irq=20, rst=15, gpio=26)

# # LoRa
# sx.begin(freq=863.75, bw=500, sf=12, cr=8, syncWord=0x34,
#          power=14, currentLimit=60.0, preambleLength=8,
#          implicit=False, implicitLen=0xFF,
#          crcOn=True, txIq=False, rxIq=False,
#          tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

# sx.setBlockingCallback(False, cb)


from machine import Pin

# Configurer GP0 en mode pull-down
gp1 = Pin(1, Pin.IN, Pin.PULL_DOWN)

# Configurer GP14 en mode pull-down
gp14 = Pin(14, Pin.IN, Pin.PULL_DOWN)

print("att")
while True:
    # Lire l'état des broches GP0 et GP14
    gp1_state = gp1.value()
    gp14_state = gp14.value()

    if gp1_state or gp14_state:
        # Afficher l'état des broches sur la console
        print(f"GPun: {gp1_state}, GPdeux: {gp14_state}")
    
    # sx.send(b'SIG1')
    
    # Attendre un peu avant de lire à nouveau
    # time.sleep(0.1)
