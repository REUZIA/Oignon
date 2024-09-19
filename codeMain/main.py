import time
from machine import Pin, I2C
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from GPSdata import GPSdata
from lora import LoRaTransceiver

mainModuleOn = 0
if __name__ == "__main__":
    # start_time = time.time()
    # ? initaliser composant
    timeWaitBoucl: float = 0.001
    # spi = SPI(0,baudrate = 10000,polarity=1,phase=0,mosi=Pin(3),sck=Pin(2),miso=Pin(4))

    sd = SDOignon(
        0,
        Pin(2),
        Pin(3),  # pas sur
        Pin(4),
        Pin(5),
        "data",
    )

    i2c = I2C(1, sda=Pin(6), scl=Pin(7))
    senAccGyr = ICM20948AccGyr(i2c)

    gp = GPSdata(1)

    lora = LoRaTransceiver(
        spi_bus=0,
        clk=26,
        mosi=27,
        miso=12,
        cs=19,
        irq=20,
        rst=15,
        gpio=20,
    )
    lora.setup(864)

    # ? maitre le composant en sleep mode
    senAccGyr.to_sleep()
    gp.to_sleep()

    print("start")
    # while True:
    #     time.sleep(timeWaitBoucl)
    #     # detecter si on veut alluer

    #     if mainModuleOn:# on allume les modules
    #         print("allumer")
    #         senAccGyr.wake_up()
    #         gp.wake_up()
    #         # pas sleep lora si on envoie pas

    #     #? quand boucle on
    #     while mainModuleOn:
    #         time.sleep(timeWaitBoucl)
    #         #? lire les datas
    #         res =""
    #         res+=str(senAccGyr)+";"+str(gp)
    #         #? envoi data
    #         # envoyer carte sd
    #         sd.add(res)
    #         # envoyer gnd station
    #         lora.send(res)
    #         #? detecter si off

    #         if not mainModuleOn:# on etteint les modules
    #             print("eteindre")
    #             senAccGyr.to_sleep()
    #             gp.to_sleep()
