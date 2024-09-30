# Initialize the shared SPI bus
from machine import Pin, SPI
from sx1262 import SX1262
import sdcard
import os
import time

# Initialize the shared SPI bus
spi = SPI(0, baudrate=2000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

# LoRa SX1262 pins
lora_cs = Pin(27, Pin.OUT)
lora_irq = Pin(20, Pin.IN)
lora_rst = Pin(15, Pin.OUT)
lora_gpio = Pin(26, Pin.OUT)

# SD card pins
sd_cs = Pin(5, Pin.OUT)

# Ensure both CS pins are high (inactive) initially
lora_cs.value(1)
sd_cs.value(1)

# Initialize LoRa
sx = None

# Initialize SD card
sd = None

def init_lora():
    global sx
    print("Initializing LoRa...")
    lora_cs.value(1)  # Ensure CS is high before starting
    
    # Reset the LoRa module
    lora_rst.value(0)
    time.sleep_ms(10)
    lora_rst.value(1)
    time.sleep_ms(10)
    
    try:
        sx = SX1262(spi_bus=0, clk=18, mosi=19, miso=16, cs=27, irq=20, rst=15, gpio=26)
        lora_cs.value(0)  # Activate LoRa CS
        sx.begin(freq=923, bw=125.0, sf=12, cr=8, syncWord=0x12,
                 power=-5, currentLimit=60.0, preambleLength=8,
                 implicit=False, implicitLen=0xFF,
                 crcOn=True, txIq=False, rxIq=False,
                 tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
        sx.setBlockingCallback(False, lora_callback)
        print("LoRa initialized successfully")
    except Exception as e:
        print(f"Error initializing LoRa: {e}")
        sx = None
    finally:
        lora_cs.value(1)  # Deactivate LoRa CS

def init_sd():
    global sd, vfs
    print("Initializing SD card...")
    try:
        sd = sdcard.SDCard(spi, sd_cs)
        vfs = os.VfsFat(sd)
        os.mount(vfs, '/sd')
        print("SD card initialized and mounted")
    except Exception as e:
        print(f"Error initializing SD card: {e}")
        sd = None

def lora_callback(events):
    if sx and events & SX1262.RX_DONE:
        lora_cs.value(0)  # Activate LoRa CS
        try:
            msg, err = sx.recv()
            error = SX1262.STATUS[err]
            print("Received LoRa message:", msg)
            print("Status:", error)
        finally:
            lora_cs.value(1)  # Deactivate LoRa CS

def send_lora_message(message):
    if sx:
        lora_cs.value(0)  # Activate LoRa CS
        try:
            sx.send(message)
            print(f"Sent LoRa message: {message}")
        finally:
            lora_cs.value(1)  # Deactivate LoRa CS
    else:
        print("LoRa not initialized, cannot send message")

def read_sd_file(filename):
    if sd:
        sd_cs.value(0)  # Activate SD card CS
        try:
            with open(filename, 'r') as file:
                content = file.read()
            print(f"Content of {filename}:", content)
        finally:
            sd_cs.value(1)  # Deactivate SD card CS
    else:
        print("SD card not initialized, cannot read file")

def write_sd_file(filename, content):
    if sd:
        sd_cs.value(0)  # Activate SD card CS
        try:
            with open(filename, 'w') as file:
                file.write(content)
            print(f"Wrote to {filename}: {content}")
        finally:
            sd_cs.value(1)  # Deactivate SD card CS
    else:
        print("SD card not initialized, cannot write file")

# Initialize LoRa and SD card
init_lora()
init_sd()

# Example usage
try:
    if sx:
        # LoRa operation
        send_lora_message(b'Hello from shared SPI!')
    
    if sd:
        # SD card operations
        write_sd_file('/sd/test.txt', 'Hello from SD card!')
        read_sd_file('/sd/test.txt')
    
    # Wait for potential LoRa response
    print("Waiting for LoRa messages...")
    time.sleep(1)  # Wait for 1 seconds to potentially receive a message

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if sd:
        # Unmount SD card
        os.umount('/sd')
        print("SD card unmounted")