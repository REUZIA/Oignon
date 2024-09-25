#https://docs.micropython.org/en/latest/library/pyb.html
import time
import os
import sdcard
from machine import Pin, I2C,SPI,UART
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from utime import sleep
from micropyGPS import MicropyGPS  # https://github.com/inmcm/micropyGPS
from lora import LoRaTransceiver


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

# ! à fair
if __name__ == "__main__":
    # ? I2C pin ICM20948 
    i2c = I2C(1, sda=Pin(6), scl=Pin(7)) # SDA : GPIO0 ; SCL : GPIO1
    sen = ICM20948AccGyr(i2c)
    sen.to_sleep()
    # print(sen.icm.sleep)
    sen.wake_up()#jsp pk sa marche pas jpp
    print(sen.icm.sleep)

    accxInit, accyInit, acczInit = sen.icm.acceleration
    gyroxInit, gyroyInit, gyrozInit = sen.icm.gyro
    accx, accy, accz = sen.icm.acceleration
    gyrox, gyroy, gyroz = sen.icm.gyro
    while accx == accxInit and accy == accyInit and accz == acczInit and gyrox == gyroxInit and gyroy == gyroyInit and gyroz == gyrozInit: 
        accx, accy, accz = sen.icm.acceleration
        gyrox, gyroy, gyroz = sen.icm.gyro
        print("att diff ICM20948")
        time.sleep(0.2)
    
    print("pass ICM20948")


    uart= UART(1,baudrate=9600, tx=Pin(4), rx=Pin(5), timeout=5000, timeout_char=5000)  # initialisation UART 1 # TX : GPIO4 ; RX : GPIO 5 
    gps = MicropyGPS() # création d'un objet GPS
    
    if uart.any():  
        donnees_brutes = str(uart.readline())
        for x in donnees_brutes:
            gps.update(x)

        print('Latitude: ' ,gps.latitude_string())
        print('Latitude (tuple): ' , gps.latitude)
        print('Longitude: ' ,gps.longitude_string())
        print('Longitude (tuple): ' , gps.longitude)
        print('Altitude: ' , gps.altitude)
        print('Vitesse: ', gps.speed_string('kph'))
        print('Date: ' , gps.date_string('s_dmy'))
        print('')
    else : 
        print("no gps data")


    # ? lora
    print("start lora  ok")
    lora = LoRaTransceiver(
        spi_bus=0,
        clk=18,
        mosi=19,
        miso=16,
        cs=27,
        irq=20,
        rst=15,
        gpio=26,
    )
    """
    ensie pine avec modif carte au ca ou
        lora = LoRaTransceiver(
            spi_bus=0,
            clk=26,
            mosi=27,
            miso=12,#16
            cs=19,
            irq=20,
            rst=15,
            gpio=20,
        )
    """
    lora.setup(863)

    lora.send("oui")
    print("lora ok")

    # ? m