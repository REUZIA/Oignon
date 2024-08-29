#https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries
#https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/neopixel-leds


# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
NeoPixel example for Pico. Turns the NeoPixels red, green, and blue in sequence.

REQUIRED HARDWARE:
* RGB NeoPixel LEDs connected to pin GP0.
"""
import time
import board
import neopixel

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 30

pixels = neopixel.NeoPixel(board.GP16, num_pixels)
pixels.brightness = 0.5

while True:
    pixels.fill((255, 0, 0))
    time.sleep(0.5)
    pixels.fill((0, 255, 0))
    time.sleep(0.5)
    pixels.fill((0, 0, 255))
    time.sleep(0.5)

