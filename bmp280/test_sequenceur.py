from machine import Pin, I2C
from utime import sleep

from bmp280 import BMP280I2C

i2c0_sda = Pin(2)
i2c0_scl = Pin(3)
i2c0 = I2C(0, sda=i2c0_sda, scl=i2c0_scl, freq=400000)
bmp280_i2c = BMP280I2C(0x77, i2c0)  # address may be different

liste_valeur=[]
var_position= 0

while True:
    #lecture
    readout = bmp280_i2c.measurements
    #print(f"Temperature: {readout['t']} °C, pressure: {readout['p']} hPa.")
    #insertion dans le tableau
    if len(liste_valeur)>10:
        liste_valeur.insert(var_position,readout['p'])
        var_position+=1
    else :
        var_position=0

    #calculer la dérivé 
    variations = [(liste_valeur[i + 1] - liste_valeur[i]) for i in range(len(liste_valeur) - 1)]


    sleep(1)