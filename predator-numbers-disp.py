"""
Requires the CircuitPython library: adafruit-circuitpython-ssd1306 module
Requires Pillow (Python Imaging Library fork)
"""

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import busio

# We need this for the pins, right now we're cheating and hard calling it.
from adafruit_blinka.board.raspberrypi.raspi_40pin import *

# There are hard coded valid I2C pins sigh.
# busyio checks these before setting up an I2C, so they must be present for all busses.
import adafruit_blinka.microcontroller.bcm283x.pin
adafruit_blinka.microcontroller.bcm283x.pin.i2cPorts = (
    (5, D22, D18), (4, D24, D23), (3, D27, D17), (1, SCL, SDA), (0, D1, D0),   
)

def displayInit(oledDisplay):
    oledDisplay.fill(0)
    oledDisplay.show()
    return

def runDisplay(oledDisplay, displayNumber):
    #oledDisplay.fill(0)
    #oledDisplay.show()

    imageFile = 'predator' + str(displayNumber) + '.bmp'

    initialImage = Image.open(imageFile)

    twoBitImage = initialImage.convert("1")

    oledDisplay.image(twoBitImage)
    oledDisplay.show()
    return

busDictionary = { 
1 : { 'SDA': SDA, 'SCL': SCL }, 
3 : { 'SDA': D17, 'SCL': D27 },
4 : { 'SDA': D23, 'SCL': D24 },
5 : { 'SDA': D18, 'SCL': D22 }
}
busNumbers = [1, 3, 4, 5]


busList = [busio.I2C(busDictionary[x]['SCL'], busDictionary[x]['SDA']) for x in busNumbers]


displayList = [adafruit_ssd1306.SSD1306_I2C(128, 64, x, addr=0x3c) for x in busList]

for i, display in enumerate(displayList):
    runDisplay(display, 1)