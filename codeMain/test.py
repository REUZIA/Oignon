from machine import Pin, SPI
import sdcard
import os
from sx1262 import SX1262
import time

# LoRa and SD chip select pins
CS_LORA = Pin(27, Pin.OUT)
CS_SD = Pin(5, Pin.OUT)

def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print('Receive: {}, {}'.format(msg, error))
    elif events & SX1262.TX_DONE:
        print('TX done.')

# LoRa setup
def init_lora():
    global sx
    # Make sure SD is not selected
    CS_SD.value(1)  # SD card inactive (CS high)
    CS_LORA.value(0)  # LoRa active (CS low)

    sx = SX1262(spi_bus=0, 
               clk=18, 
               mosi=19, 
               miso=16, 
               cs=27, 
               irq=20, #DIO1
               rst=15, #reset
               gpio=26) #busy

    sx.begin(freq=869.75, bw=500.0, sf=12, cr=8, syncWord=0x12,
             power=-5, currentLimit=60.0, preambleLength=8,
             implicit=False, implicitLen=0xFF,
             crcOn=True, txIq=False, rxIq=False,
             tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

    sx.setBlockingCallback(False, cb)

    return sx  # Return the LoRa object so we can reset it later

# SD card setup
def sdtest():
    # Ensure LoRa is not selected
    CS_LORA.value(1)  # LoRa inactive (CS high)
    CS_SD.value(0)    # SD active (CS low)

    spi = SPI(0, baudrate=10000, polarity=1, phase=0, mosi=Pin(3), sck=Pin(2), miso=Pin(4))
    spi.init()  # Ensure right baudrate
    sd = sdcard.SDCard(spi, Pin(5))  # Compatible with PCB
    vfs = os.VfsFat(sd)
    try:
        os.mount(vfs, "/fc")
        print("Filesystem check")
        print(os.listdir("/fc"))

        line = "abcdefghijklmnopqrstuvwxyz\n"
        lines = line * 100  # 2700 chars
        short = "1234567890\n"

        fn = "/fc/rats.txt"
        print()
        print("Multiple block read/write")
        with open(fn, "w") as f:
            n = f.write(lines)
            print(n, "bytes written")
            n = f.write(short)
            print(n, "bytes written")
            n = f.write(lines)
            print(n, "bytes written")

        with open(fn, "r") as f:
            result1 = f.read()
            print(len(result1), "bytes read")

        fn = "/fc/rats.txt"
        print()
        print("Single block read/write")
        with open(fn, "w") as f:
            n = f.write(short)  # one block
            print(n, "bytes written")

        with open(fn, "r") as f:
            result2 = f.read()
            print(len(result2), "bytes read")
    
    finally:
        os.umount("/fc")  # Ensure the SD card is unmounted
        CS_SD.value(1)    # Deactivate SD card

    print()
    print("Verifying data read back")
    success = True
    if result1 == "".join((lines, short, lines)):
        print("Large file Pass")
    else:
        print("Large file Fail")
        success = False
    if result2 == short:
        print("Small file Pass")
    else:
        print("Small file Fail")
        success = False
    print()
    print("Tests", "passed" if success else "failed")

def reset_lora(sx):
    """ Function to reset the LoRa module """
    sx.reset()
    CS_LORA.value(1)  # Set CS to high to deactivate LoRa
