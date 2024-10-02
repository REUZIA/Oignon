from sx1262 import SX1262
import time

import machine
from utime import sleep
from micropyGPS import MicropyGPS  # https://github.com/inmcm/micropyGP

from machine import Pin, I2C
import icm20948

import os
import sdcard

def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print(msg)
        print(error)

# Initialisation de la carte SD

spi = machine.SPI(0, baudrate=10000, polarity=1, phase=0, sck=machine.Pin(2), mosi=machine.Pin(3), miso=machine.Pin(4))

cs = machine.Pin(5, machine.Pin.OUT)

sd = sdcard.SDCard(spi, cs)

# LoRa
sx = SX1262(spi_bus=0, clk=2, mosi=3, miso=4, cs=27, irq=20, rst=15, gpio=26)

sx.begin(freq=863.75, bw=125.0, sf=12, cr=8, syncWord=0x12,
        power=-5, currentLimit=60.0, preambleLength=8,
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

sx.send(b'SIG1')

#Test carte sd



# Montage du système de fichiers SD
os.mount(sd, "/sd")

# Vérification du contenu de la carte SD (facultatif)
print("Contenu de la carte SD:", os.listdir("/sd"))

# Écriture d'un fichier sur la carte SD
with open("/sd/mon_fichier.txt", "w") as fichier:
    fichier.write("Bonjour depuis la carte SD !")

print("Écriture terminée avec succès.")

# Démontage de la carte SD
os.umount("/sd")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#GPS
uart= machine.UART(1,baudrate=9600)  # initialisation UART
gps = MicropyGPS() # création d'un objet GPS

for i in range(10):
    if uart.any():  # si nous avons reçu quelque chose...
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

    sleep(.1)


# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT



#icm20948

#test accelero
i2c = I2C(1, sda=Pin(6), scl=Pin(7))  # Correct I2C pins for RP2040
icm = icm20948.ICM20948(i2c)

icm.accelerometer_range = icm20948.RANGE_2G
icm.gyro_full_scale = icm20948.FS_250_DPS

for i in range(2):
    accx, accy, accz = icm.acceleration
    print(f"x:{accx:.2f}m/s², y:{accy:.2f}m/s², z:{accz:.2f}m/s²")
    print()
    time.sleep(0.5)
        
#test gyro

for i in range(2):
    gyrox, gyroy, gyroz = icm.gyro
    print("x:{:.2f}°/s, y:{:.2f}°/s, z:{:.2f}°/s".format(gyrox, gyroy, gyroz))
    print()
    time.sleep(0.5)
        
        
