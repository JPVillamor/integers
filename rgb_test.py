# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D21

# The number of NeoPixels
num_pixels = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

OFF = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#while True:
    # Comment this line out if you have RGBW/GRBW NeoPixels
pixels.fill(OFF)
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    # pixels.fill((255, 0, 0, 0))
pixels.show()
time.sleep(1)

from random import randint

while True:
    threshold = randint(0,200)
    print(threshold)
    
    if threshold >= 100:
        pixels[1] = RED
    elif threshold<100:
        pixels[1] = OFF
        
    pixels.show()
    time.sleep(2)