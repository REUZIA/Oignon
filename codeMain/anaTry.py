import time
from machine import Pin, SPI, reset
import sdcard
import os
from sx1262 import SX1262  # Assuming you have an SX1262 MicroPython driver

# Function to reset the SX1262 module
def reset_sx1262(reset_pin):
    print("Resetting SX1262...")
    reset_pin.value(0)
    time.sleep(0.01)  # 10 ms delay
    reset_pin.value(1)
    time.sleep(0.01)  # Give some time for the reset to complete

# Function to reset the SPI bus
def reset_spi(spi):
    print("Resetting SPI bus...")
    spi.deinit()  # Deinitialize SPI
    time.sleep(0.1)  # Small delay to allow the bus to reset
    spi.init()  # Reinitialize the SPI bus
    print("SPI bus reinitialized.")

# Initialize the reset pin for SX1262
reset_pin = Pin(15, Pin.OUT)
reset_sx1262(reset_pin)  # Perform a reset before initializing LoRa

# Initialize SPI for SD card and LoRa (shared SPI bus)
spi = SPI(0, baudrate=10000, polarity=1, phase=0, mosi=Pin(3), sck=Pin(2), miso=Pin(4))

# Reset SPI bus before initializing SX1262
reset_spi(spi)

# Initialize LoRa SX1262
sx = SX1262(spi_bus=0,
            clk=18,
            mosi=19,
            miso=16,
            cs=27,
            irq=20,  # DIO1
            rst=15,  # Reset
            gpio=26)  # Busy

# Configure LoRa settings
sx.begin(freq=869.75, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

sx.setBlockingCallback(False, lambda event: print("LoRa event"))

# Reset SPI again before initializing the SD card
reset_spi(spi)

# Initialize SD card
sd = sdcard.SDCard(spi, Pin(5))  # Pin 5 is CS for the SD card
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

# Define a function to write the message to the SD card
def write_to_sd(message):
    try:
        with open("/sd/messages.txt", "a") as file:  # Open file in append mode
            file.write(message + "\n")
        print("Message written to SD card.")
    except Exception as e:
        print("Failed to write to SD card:", e)

# Function to send a message over LoRa
def send_lora_message(message):
    sx.send(bytes(message, 'utf-8'))
    print(f"LoRa message sent: {message}")

# Example message to transmit and save
message = "Hello LoRa!"

# Send the message via LoRa
send_lora_message(message)

# Save the message to the SD card
write_to_sd(message)

# Pause to ensure operations complete
time.sleep(2)

# Unmount SD card
os.umount("/sd")