import time
from machine import Pin, I2C
from mainICM20948 import ICM20948Sensor

mainModuleOn = 0
if __name__ == "__main__":
    #? initaliser composant 
    i2c = I2C(0, sda=Pin(0), scl=Pin(1))
    sen = ICM20948Sensor(i2c)
    #? allumer
    while True:
        time.usleep(250)
        # detecter si on veut alluer 
            # on allume les modules
        #? quand boucle on 
        while mainModuleOn:
            #? detecter si off
                # on etteint les modules
            #? lire les datas
            res =""
            res+=str(sen)+";"
            #? envoi data
            # envoyer carte sd
            # envoyer gnd station
            pass
