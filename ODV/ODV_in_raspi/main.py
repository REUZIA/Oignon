import time
from machine import Pin, I2C
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from GPSdata import GPSdata
from LoRaTransceiver import LoRaTransceiver
import gc

gc.enable()

toggelApo:bool = False
toggelAll:bool = False
toggelEte:bool = False

def apoger(pin) -> None:
    global sd,toggelApo
    """_summary_
        fonction appeler à l'appoger
        elle vas stocker le temps (du gps) dans un le fichier APOGER.csv
    """
    print("interup apoger")
    if not toggelApo:
        toggelApo = True
        # on écire apoger 
        res = str(gp).split(";")[-1]
        res = f"\nAPOGER;{res}\n"

        # envoyer carte sd
        sd.write(res)
        # envoyer gnd station
        lora.send(res)
         
        # Désactiver l'interruption
        gpAllumer.irq(handler=None)

# detecter si on veut alluer
def allumer(pin)->None:
    print("interup allumer")
    global mainModuleOn,toggelAll,toggelEte
    if not toggelAll:
        toggelAll = True
        toggelEte = False

        mainModuleOn = True

# detecter si on veut eteindre
def eteindre(pin)->None:
    print("interup eteindre")
    global mainModuleOn,toggelAll,toggelEte
    if not toggelEte:
        # on dit que c etein pour l'interup
        toggelAll = False
        toggelEte = True
        # on fait eteindre dans la boucle 
        mainModuleOn = False

if __name__ == "__main__":
    # ? initaliser composant
    timeWaitBoucl: float = 0.2
    mainModuleOn = 0

    #! SD
    sd = SDOignon(
        nbspi=0,
        baudrate=2000000,
        pinSck=2,
        pinMiso=4,
        pinMosi=3,
        pinSC=5,
        fichierName="mainData",
        colmSvg="accelero;gyro;autre",
    )

    # ! ICM
    senAccGyr = ICM20948AccGyr(i2c_bus=1,sda_nbPin=6,scl_nbPin=7)
    senAccGyr.wake_up()

    #! GPS
    gp = GPSdata(1, rx=9, tx=8)

    # ! LORA
    lora = LoRaTransceiver(
        spi_bus=0,
        clk=2,
        mosi=3,
        miso=4,
        cs=27,
        irq=20,
        rst=15,
        gpio=26,
    )
    lora.setup(869.75, bw=500, sf=12, cr=8, power=14)


    gc.collect()

    # ? set up interupt
        # ? laison montante
    gpAllumer = Pin(1, Pin.IN, Pin.PULL_DOWN)
    gpAllumer.irq(trigger=Pin.IRQ_RISING, handler=allumer)
    gpEteindre = Pin(14, Pin.IN, Pin.PULL_DOWN)
    gpEteindre.irq(trigger=Pin.IRQ_RISING, handler=eteindre)
        # ? altimetrique
    gpApoger = Pin(0, Pin.IN, Pin.PULL_DOWN)
    gpApoger.irq(trigger=Pin.IRQ_RISING, handler=apoger)

    # ? maitre le composant en sleep mode
    senAccGyr.to_sleep()
    gp.to_sleep()

    iswakepup:bool = False
    print("start")
    # mainModuleOn=True#!debug
    while True:
        time.sleep(timeWaitBoucl)
        
        if mainModuleOn:  # on allume les modules
            print("allumer")
            senAccGyr.wake_up()
            gp.wake_up()
            iswakepup = True
            # pas sleep lora si on envoie pas
            time.sleep(1)

        # ? quand boucle on
        while mainModuleOn and iswakepup:
            time.sleep(timeWaitBoucl)
            # ? lire les datas
            res = ""
            res += str(senAccGyr) + ";" + str(gp)
            # print("res:", res) # ! debug
            # ? envoi data
            # envoyer carte sd
            sd.write(res)
            # envoyer gnd station
            lora.send(res)

            # ? si off
            if not mainModuleOn :  # on etteint les modules
                print("eteindre")
                mainModuleOn = False
                senAccGyr.to_sleep()
                gp.to_sleep()
                iswakepup:bool = False
