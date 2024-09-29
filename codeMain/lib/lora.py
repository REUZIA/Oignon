"""
spi_bus : 1
clk : 10 = 14
mosi : 11 = 15
miso : 12 = 16
cs : 3 = 5
irq ;DIO1 : 20 = 26
rst;Rest : 15 = 20
gpio;BUSY : 2 = 4

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)
https://github.com/ehong-tl/micropySX126X?tab=readme-ov-file

"""

from sx1262 import SX1262
import time
from machine import Pin, SPI



class LoRaTransceiver:
    def __init__(
        self,
        spi_bus=1,
        clk=10,#sck
        mosi=11,
        miso=12,
        cs=3,
        irq=20,#DIO1
        rst=15,#Rest
        gpio=2,#BUSY
    ):
        self.sx = SX1262(
            spi_bus=spi_bus,
            clk=clk,#sck
            mosi=mosi,
            miso=miso,
            cs=cs,
            irq=irq,#DIO1
            rst=rst,#Rest
            gpio=gpio,#BUSY
        )
        self.received_data = None
    def callback(self, events):
        if events & SX1262.RX_DONE:
            self.received_data, err = self.sx.recv()
            error = SX1262.STATUS[err]
            print("Received: {}, {}".format(self.received_data, error))
        elif events & SX1262.TX_DONE:
            print("TX done.")

    def setup(self,freq:float) -> None:
        # LoRa
        self.sx.begin(
            freq=freq,
            bw=500.0,
            sf=12,
            cr=8,
            syncWord=0x12,
            power=-5,
            currentLimit=60.0,
            preambleLength=8,
            implicit=False,
            implicitLen=0xFF,
            crcOn=True,
            txIq=False,
            rxIq=False,
            tcxoVoltage=1.7,
            useRegulatorLDO=False,
            blocking=True,
        )

        self.sx.setBlockingCallback(False, self.callback)

    def send(self, text: str) -> None:
        self.sx.send(b"{text}")

    def recive(self) -> str:
        res = ""
        if self.received_data:
            res = self.received_data
            self.received_data = None
        return res


if __name__ == "__main__":
    CS_LORA = Pin(27, Pin.OUT)
    CS_SD = Pin(5, Pin.OUT)
    CS_LORA.value(0)  # LoRa active
    CS_SD.value(1)    # SD inacte

    lora = LoRaTransceiver(
        spi_bus = 0,
        clk = 18,
        mosi = 19,
        miso = 16,
        cs = 27,
        irq = 20,#DIO1
        rst = 15,#reset
        gpio = 26,#busy
    )
    lora.setup(869.75)

    while True:
        lora.send("Ping")
        time.sleep(10)
