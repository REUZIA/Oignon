import time
from machine import Pin, I2C
from ICM20948AccGyr import ICM20948AccGyr
from SDOignon import SDOignon
from GPSdata import GPSdata
from LoRaTransceiver import LoRaTransceiver
import gc

if __name__ == "__main__":
    
    #! SD
    sd = SDOignon(
        nbspi = 0,
        baudrate = 2000000,
        pinSck = 2,
        pinMiso = 4, 
        pinMosi = 3,
        pinSC = 5,
        fichierName = "test",
        colmSvg = "accelero;gyro"
    )
    
    # ! ICM 
    i2c = I2C(1, sda=Pin(6), scl=Pin(7))
    senAccGyr = ICM20948AccGyr(i2c)
    senAccGyr.wake_up()

    #! GPS
    gp = GPSdata(1, rx=9, tx=8)

    # ! LORA
    lora = LoRaTransceiver(
        spi_bus = 0,
        clk = 2,
        mosi = 3,
        miso = 4,
        cs = 27,
        irq = 20,
        rst = 15,
        gpio = 26,
    )
    lora.setup(869.75,sf=12,cr=8)
    
    gc.collect()
    
    # ! test solo SD 
    # for _ in range(100):
    for _ in range(10):
        sd.write("1:2:3;4:5:6s")
        time.sleep(0.1)

    # ! test solo ICM    
    print("start ICM")
    for _ in range(10):
        print(senAccGyr)
        time.sleep(0.1)
    print("end ICM")

    # ! test solo GPS 
    for _ in range(3):
        print(gp)
        time.sleep(1)
    print("end ICM")

    # ! test solo LORA
    print("start LORA")
    line = "abcdefghijklmnopqr\n"
    for _ in range(10):     
        lora.send(line)
        time.sleep(1)
    print("end LORA")

    # ! test lora + sd
    print("start LORA+SD")
    line = "-0.07:-0.14:9.87;0.01:0.00:0.00;48:48:50.9:N;2:22:40.6:E;89.5;6;8;0.118528;10:31:35.0"
    for _ in range(100):  
        sd.write(line)
        lora.send(line)
        time.sleep(0.1)
    print("end LORA")
