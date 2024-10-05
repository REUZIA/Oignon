import machine
from utime import sleep
from micropyGPS import MicropyGPS  # https://github.com/inmcm/micropyGPS

uart= machine.UART(1,baudrate=9600)  # initialisation UART
gps = MicropyGPS() # création d'un objet GPS

while True:
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