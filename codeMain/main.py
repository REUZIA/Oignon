import time
from machine import Pin, I2C
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from GPSdata import GPSdata

mainModuleOn = 0
if __name__ == "__main__":
    # start_time = time.time()
    #? initaliser composant 
    timeWaitBoucl:float=0.001

    sd = SDOignon(
        1,
        Pin(10),
        Pin(11),
        Pin(12),
        Pin(13),
        "data.txt",
    )

    i2c = I2C(0, sda=Pin(0), scl=Pin(1))
    senAccGyr = ICM20948AccGyr(i2c)
    
    gp = GPSdata(1)

    #? maitre le composant en sleep mode 
    senAccGyr.to_sleep()
    gp.to_sleep()

    while True:
        time.sleep(timeWaitBoucl)
        # detecter si on veut alluer 
        if mainModuleOn:# on allume les modules
            print("allumer")
            senAccGyr.wake_up()
            gp.wake_up()
            # sleep ?
        
        #? quand boucle on 
        while mainModuleOn:
            time.sleep(timeWaitBoucl)
            #? lire les datas
            res =""
            res+=str(senAccGyr)+";"+str(gp)
            #? envoi data
            # envoyer carte sd
            sd.add(res)
            # envoyer gnd station
            #? detecter si off

            if not mainModuleOn:# on etteint les modules
                print("eteindre")
                senAccGyr.to_sleep()
                gp.to_sleep()


