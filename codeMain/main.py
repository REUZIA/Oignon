import time
from machine import Pin, I2C
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon


mainModuleOn = 0
if __name__ == "__main__":
    start_time = time.time()
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
    

    #? maitre le composant en sleep mode 
    senAccGyr.to_sleep()

    testi=0
    nbbloucle=100
    while True:
        testi+=1
        time.sleep(timeWaitBoucl)
        # detecter si on veut alluer 
        if testi>4:
            break
        if testi>3:
            mainModuleOn=True
        if mainModuleOn:# on allume les modules
            print("allumer")
            senAccGyr.to_awake()
        
        #? quand boucle on 
        while mainModuleOn:
            testi+=1
            time.sleep(timeWaitBoucl)
            #? lire les datas
            res =""
            res+=str(senAccGyr)+";"
            #? envoi data
            # envoyer carte sd
            sd.add(res)
            # envoyer gnd station
            #? detecter si off
            if testi>nbbloucle:
                mainModuleOn=False
            if not mainModuleOn:# on etteint les modules
                print("eteindre")
                senAccGyr.to_sleep()
    st = sd.read()
    sd.umount()
    end_time = time.time()
    time_run:float = end_time - start_time
    print(f"Temps d'exécution: {time_run} secondes")
    print(st)


