import time
import os
import sdcard
from machine import Pin, I2C,SPI,UART
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from utime import sleep
from micropyGPS import MicropyGPS  # https://github.com/inmcm/micropyGPS

def sdtest():
    spi = SPI(1,baudrate = 10000,polarity=1,phase=0,mosi=Pin(11),sck=Pin(10),miso=Pin(12))
    spi.init()  # Ensure right baudrate
    sd = sdcard.SDCard(spi, Pin(13))  # Compatible with PCB
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/fc")
    print("Filesystem check")
    print(os.listdir("/fc"))

    line = "abcdefghijklmnopqrstuvwxyz\n"
    lines = line * 200  # 5400 chars
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

    fn = "/fc/rats1.txt"
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
    # I2C pin ICM20948 
    i2c = I2C(0, sda=Pin(0), scl=Pin(1)) # SDA : GPIO0 ; SCL : GPIO1
    sen = ICM20948AccGyr(i2c)
    sen.to_sleep()
    print(sen.icm.sleep)
    sen.to_awake()
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

    sdtest() # CS : GPIO10 ; mosi : GPIO11,SCK : GPIO10,miso : GPIO12 

    uart= UART(1,baudrate=9600)  # initialisation UART 1 # TX : GPIO4 ; RX : GPIO 5 
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
