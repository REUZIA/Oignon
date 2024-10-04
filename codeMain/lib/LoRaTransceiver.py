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
        self.spi_bus=spi_bus
        self.clk=clk
        self.mosi=mosi
        self.miso=miso
        self.cs=cs
        self.irq=irq
        self.rst=rst
        self.gpio=gpio

        self.received_data = None
        self.nbPaquerEnvoyer:int = 0
        self.isInit:bool = False
        
        self.pasTermineEnvoyer:bool = False

        self.init()

        
    def init(self)->None:
        try : 
            self.isInit:bool = True
            self.sx = SX1262(
                spi_bus=self.spi_bus,
                clk=self.clk,#sck
                mosi=self.mosi,
                miso=self.miso,
                cs=self.cs,
                irq=self.irq,#DIO1
                rst=self.rst,#Rest
                gpio=self.gpio,#BUSY
            )
        except:
            print("erreur init lora ")
            self.isInit:bool = False
            
    def callback(self, events)->None:

        if events & SX1262.RX_DONE:
            self.received_data, err = self.sx.recv()
            error = SX1262.STATUS[err]
            print("Received: {}, {}".format(self.received_data, error))
        elif events & SX1262.TX_DONE:
            print("TX done.")
            self.pasTermineEnvoyer = False
            self.nbPaquerEnvoyer += 1

    def setup(self,freq:float,bw:float=500,sf=12,cr=8,syncWork=0x34,power=14) -> bool:
        erreur:bool = False
        if self.isInit:
            try :
                # LoRa
                self.sx.begin(
                    freq=freq,#869.75
                    bw=bw,
                    sf=sf,
                    cr=cr,
                    syncWord=syncWork,
                    power=power,
                    currentLimit=60.0,
                    preambleLength=8,
                    implicit=False,
                    implicitLen=0xFF,
                    crcOn=True,
                    txIq=False,
                    rxIq=False,
                    useRegulatorLDO=False,
                    blocking=True,
                )

                self.sx.setBlockingCallback(False, self.callback)
            except:
                self.isInit:bool = False
                erreur:bool = True
        return not erreur

    def send(self, text: str) -> None:
        try :
            if not self.pasTermineEnvoyer:
                self.pasTermineEnvoyer = True
                print("byte :",self.sx.send(text.encode()))
        except:
            print("erreur lora")
            pass

    def recive(self) -> str:
        res = ""
        if self.received_data:
            res = self.received_data
            self.received_data = None
        return res


if __name__ == "__main__":

    lora = LoRaTransceiver(
        spi_bus = 0,
        clk = 2,
        mosi = 3,
        miso = 4,
        cs = 27,
        irq = 20,#DIO1
        rst = 15,#reset
        gpio = 26,#busy
    )
    # lora.setup(869.75,bw=500)
    lora.setup(869.75,bw=500,sf=12,cr=8)
    print("end init")
    # while True:
    for _ in range(100):
        print("send")
        # lora.send("-0.07:-0.14:9.87;0.01:0.00:0.00;48:48:50.9:N;2:22:40.6:E;89.5;6;8;0.118528;10:31:35.0")
        
        lora.send(f"[{_}]-0.07:-0.14:9.87;0.01:0.00:0.00;48:48:50.9:N;2:22:40.6:E;89.5;6;8;0.118528;10:31:35.0")
        # lora.send(f"-0.07:{10**_}")
        time.sleep(0.1)
