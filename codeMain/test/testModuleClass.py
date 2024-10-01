import time
from machine import Pin, I2C
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from GPSdata import GPSdata
from lora import LoRaTransceiver

if __name__ == "__main__":
    
    # #! SD
    # sd = SDOignon(
    #     nbspi = 0,
    #     baudrate = 10000,
    #     pinSck = 18,
    #     pinMiso = 16, 
    #     pinMosi = 19,
    #     pinSC = 5,
    #     fichierName = "test",
    #     colmSvg = "accelero;gyro"
    # )
    
    # # ! ICM 
    # i2c = I2C(1, sda=Pin(6), scl=Pin(7))
    # senAccGyr = ICM20948AccGyr(i2c)
    # senAccGyr.wake_up()

    # #! GPS
    # gp = GPSdata(1, rx=9, tx=8)

    # ! LORA
    lora = LoRaTransceiver(
        spi_bus = 0,
        clk = 18,
        mosi = 19,
        miso = 16,
        cs = 27,
        irq = 20,
        rst = 15,
        gpio = 26,
    )
    lora.setup(869.75)

    # # ! test solo SD 
    # for _ in range(10):
    #     sd.write("1:2:3;4:5:6s")
    #     time.sleep(0.1)

    # # ! test solo ICM    
    # print("start ICM")
    # for _ in range(10):
    #     print(senAccGyr)
    #     time.sleep(0.1)
    # print("end ICM")

    # # ! test solo GPS 
    # for _ in range(3):
    #     print(gp)
    #     time.sleep(1)
    # print("end ICM")

    # # ! test solo LORA
    # print("start LORA")
    # line = "abcdefghijklmnopqr\n"
    # for _ in range(10):     
    #     lora.send(line)
    #     time.sleep(1)
    # print("end LORA")

    