import time
from machine import Pin, I2C
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from GPSdata import GPSdata
from LoRaTransceiver import LoRaTransceiver
import gc

gc.enable()

def test(nbtest: int) -> None:
    global lora
    """test les lora

    Args:
        nbtest (int): c le numéro du test
    """

    freq: float = 869.75
    timeAtt:float = 0.1
    if nbtest == 0:  # j'att de recevoir
        return None
    elif nbtest == 1:
        lora.setup(freq, bw=500, sf=12, cr=8, power=14)
    elif nbtest == 2:
        lora.setup(freq, bw=250, sf=12, cr=8, power=14)
    elif nbtest == 3:
        lora.setup(freq, bw=125, sf=12, cr=8, power=14)
        timeAtt=0.2
    elif nbtest == 4:
        lora.setup(freq, bw=500, sf=9, cr=8, power=14)
    elif nbtest == 5:
        lora.setup(freq, bw=500, sf=7, cr=8, power=14)
    elif nbtest == 6:
        lora.setup(freq, bw=500, sf=12, cr=6, power=14)
    elif nbtest == 7:
        lora.setup(freq, bw=500, sf=12, cr=5, power=14)
    elif nbtest == 8:
        lora.setup(freq, bw=500, sf=12, cr=8, power=7)
    elif nbtest == 9:
        lora.setup(freq, bw=500, sf=12, cr=8, power=2)
    else:
        # stop car pas argument
        print("pas bon argument")
        return None
    
    gc.collect()

    time.sleep(1)
    print("send")
    stopAtSomePoint = 0

    while lora.nbPaquerEnvoyer < 25 and stopAtSomePoint < 150:  # 15s max
        # recupérai donner gps + ICM
        res: str = "-0.07:-0.14:9.87;0.01:0.00:0.00;48:48:50.9:N;2:22:40.6:E;89.5;6;8;0.118528;10:31:35.0"# str(senAccGyr) + ";" + str(gp) + ";" + str(stopAtSomePoint)
        # sd.write(res)
        lora.send(res)
        stopAtSomePoint += 1
        time.sleep(timeAtt)

    # sd.umount()

if __name__ == "__main__":
    # # ! SD
    # sd = SDOignon(
    #     nbspi=0,
    #     baudrate=2000000,
    #     pinSck=2,
    #     pinMiso=4,
    #     pinMosi=3,
    #     pinSC=5,
    #     fichierName="",
    #     colmSvg="accelero;gyro;latitude;longitude;altitude;nombre_satellite_utiliser;nombre_satellite_visible;vitesse;heure;nbpaker",
    # )

    # # ! ICM
    # i2c = I2C(1, sda=Pin(6), scl=Pin(7))
    # senAccGyr = ICM20948AccGyr(i2c)
    # senAccGyr.wake_up()

    # #! GPS
    # gp = GPSdata(1, rx=9, tx=8)

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



    test(3)
    print(lora.nbPaquerEnvoyer)
