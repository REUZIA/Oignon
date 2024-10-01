import time
from machine import Pin, I2C
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from GPSdata import GPSdata
from lora import LoRaTransceiver


def apoger() -> None:
    global sd
    """_summary_
        fonction appeler à l'appoger
        elle vas stocker le temps (du gps) dans un le fichier APOGER.csv
    """
    # on vas fermer la sd
    sd.fich.fermet()
    # lire date gps
    date = "19h34"
    # on écrire un fichier
    with open("apoger.txt", "w") as file:
        file.write(f"apoger en : {date}")
    # on le réécrit
    sd.fich.ouvrir()


if __name__ == "__main__":
    # ? initaliser composant
    timeWaitBoucl: float = 1  # 0.01
    mainModuleOn = 0

    sd = SDOignon(
        nbspi=0,
        baudrate=10000,
        pinSck=2,
        pinMiso=4,
        pinMosi=3,
        pinSC=5,
        fichierName="data",
        colmSvg="",
    )

    i2c = I2C(1, sda=Pin(6), scl=Pin(7))
    senAccGyr = ICM20948AccGyr(i2c)

    gp = GPSdata(1, baudRate=9600, tx=4, rx=5)

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
    lora.setup(869.75)

    # ? set up interupt
    # Configurer le GPIO 13 en entrée avec une interruption sur front montant
    pin13 = Pin(13, Pin.IN, Pin.PULL_DOWN)
    pin13.irq(trigger=Pin.IRQ_RISING, handler=apoger)

    # ? maitre le composant en sleep mode
    senAccGyr.to_sleep()
    gp.to_sleep()

    print("start")
    i = 0  # TODO debug
    while True:
        i += 1  # TODO debug
        time.sleep(timeWaitBoucl)
        # detecter si on veut alluer
        if i == 1:  # TODO debug
            mainModuleOn = True

        if mainModuleOn:  # on allume les modules
            print("allumer")
            senAccGyr.wake_up()
            gp.wake_up()
            # pas sleep lora si on envoie pas
            time.sleep(1)

        # ? quand boucle on
        while mainModuleOn:
            time.sleep(timeWaitBoucl)
            # ? lire les datas
            res = ""
            res += str(senAccGyr) + ";" + str(gp)
            print("res:", res)
            # ? envoi data
            # envoyer carte sd
            sd.write(res)
            # envoyer gnd station
            lora.send(res)

            # ? detecter si off
            if not mainModuleOn:  # on etteint les modules
                print("eteindre")
                mainModuleOn = 0
                senAccGyr.to_sleep()
                gp.to_sleep()
