import time
from machine import Pin, SPI, reset
import sdcard
import os
from sx1262 import SX1262

# Global variables for resources that need cleanup
sx = None
sd = None
spi_lora = None
spi_sd = None

def init_lora():
    global sx, spi_lora
    
    # Initialize SPI for LoRa
    spi_lora = SPI(0, baudrate=10000000, polarity=0, phase=0, bits=8,
                   sck=Pin(18), mosi=Pin(19), miso=Pin(16))
    
    # Reset SX1262
    reset_pin = Pin(15, Pin.OUT)
    reset_pin.value(0)
    time.sleep(0.01)
    reset_pin.value(1)
    time.sleep(0.01)

    # Initialize LoRa SX1262
    sx = SX1262(spi_bus=0,
                clk=18,
                mosi=19,
                miso=16,
                cs=27,
                irq=20,
                rst=15,
                gpio=26)

    # Configure LoRa settings
    sx.begin(freq=869.75, bw=500.0, sf=12, cr=8, syncWord=0x12,
             power=-5, currentLimit=60.0, preambleLength=8,
             implicit=False, implicitLen=0xFF,
             crcOn=True, txIq=False, rxIq=False,
             tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

    sx.setBlockingCallback(False, lambda event: print("LoRa event"))
    print("LoRa initialized")

def init_sd():
    global sd, spi_sd
    
    # Initialize SPI for SD card
    spi_sd = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    
    # Initialize SD card
    sd = sdcard.SDCard(spi_sd, Pin(5))
    os.mount(sd, "/sd")
    print("SD card initialized")

def write_to_sd(message):
    try:
        with open("/sd/messages.txt", "a") as file:
            file.write(message + "\n")
        print("Message written to SD card.")
    except Exception as e:
        print("Failed to write to SD card:", e)

def send_lora_message(message):
    sx.send(bytes(message, 'utf-8'))
    print(f"LoRa message sent: {message}")

def cleanup():
    global sx, sd, spi_lora, spi_sd
    
    if sx:
        sx.sleep()  # Put LoRa module to sleep
    
    if "/sd" in os.listdir("/"):
        os.umount("/sd")
        print("SD card unmounted")
    
    if spi_lora:
        spi_lora.deinit()
    
    if spi_sd:
        spi_sd.deinit()
    
    # Reset global variables
    sx = None
    sd = None
    spi_lora = None
    spi_sd = None

def soft_reset():
    print("Performing soft reset...")
    time.sleep(1)  # Give some time for the message to be printed
    reset()

def main():
    try:
        init_lora()
        init_sd()

        message = "Hello LoRa"
        for i in range(20):
            send_lora_message(message)
            write_to_sd(message)

        time.sleep(2)
    finally:
        cleanup()
    soft_reset()

if __name__ == "__main__":
    main()