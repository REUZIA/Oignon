from machine import Pin, SPI
from sx1262 import SX1262

def cb(events):
    if events & SX1262.RX_DONE:
        msg, err = sx.recv()
        error = SX1262.STATUS[err]
        print(msg)
        print(error)
        
# Initialize SPI
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

# LoRa SX1262 pins
lora_cs = Pin(27, Pin.OUT)
lora_irq = Pin(20, Pin.IN)
lora_rst = Pin(15, Pin.OUT)
lora_gpio = Pin(26, Pin.OUT)

# Initialize LoRa
sx = SX1262(spi_bus=0, clk=18, mosi=19, miso=16, cs=lora_cs, irq=lora_irq, rst=lora_rst, gpio=lora_gpio)

sx.setBlockingCallback(False, cb)

# Test available methods
print("Available methods:")
print(dir(sx))

# Try some basic operations
try:
    print("Attempting to enter standby mode...")
    sx.standby()
    print("Standby mode entered successfully")
except Exception as e:
    print(f"Error entering standby mode: {e}")

try:
    print("Attempting to send data...")
    sx.send(b'Test message')
    print("Data sent successfully")
except Exception as e:
    print(f"Error sending data: {e}")

try:
    print("Attempting to receive data...")
    data = sx.receive()
    print(f"Received data: {data}")
except Exception as e:
    print(f"Error receiving data: {e}")