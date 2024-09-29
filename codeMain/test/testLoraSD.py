import time
from machine import Pin, I2C,SPI
# from SDOignon import SDOignon
import sdcard
import os
from sx1262 import SX1262
import time

def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print('Receive: {}, {}'.format(msg, error))
    elif events & SX1262.TX_DONE:
        print('TX done.')

sx = SX1262(spi_bus=0, 
           clk=18, 
           mosi=19, 
           miso=16, 
           cs=27, 
           irq=20, #DIO1
           rst=15, #reset
           gpio=26) #busy





def sdtest():
    spi = SPI(0,baudrate = 10000,polarity=1,phase=0,mosi=Pin(3),sck=Pin(2),miso=Pin(4))
    spi.init()  # Ensure right baudrate
    sd = sdcard.SDCard(spi, Pin(5))  # Compatible with PCB
    vfs = os.VfsFat(sd)
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

    os.umount("/fc")

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


if __name__ == "__main__":
    sdtest()

    # LoRa
sx.begin(freq=869.75, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

sx.setBlockingCallback(False, cb)
    # while True:
    #     sx.send(b'Ping')
    #     time.sleep(10)
    #! SD
    # sd = SDOignon(
    #     nbspi = 0,
    #     baudrate = 10000,
    #     pinSck = 2,
    #     pinMiso = 4, 
    #     pinMosi = 3,
    #     pinSC = 5,
    #     fichierName = "test",
    #     colmSvg = "accelero;gyro"
    # )
    # ! LORA
    # lora = LoRaTransceiver(
    #     spi_bus = 0,
    #     clk = 18,
    #     mosi = 19,
    #     miso = 16,
    #     cs = 27,
    #     irq = 20,
    #     rst = 15,
    #     gpio = 26,
    # )
    # lora.setup(869.75)

    # ! test solo SD 
    # for _ in range(10):
    #     sd.write("1:2:3;4:5:6s")
    #     time.sleep(0.1)

    # ! test solo LORA
    # line = "abcdefghijklmnopqrstuvwxyz\n"
    # for _ in range(10):
    #     lora.send(line)
    #     time.sleep(0.1)

# while True:
#     sx.send(b'Ping')
#     time.sleep(10)
