"""
Requires the CircuitPython library: adafruit-circuitpython-ssd1306 module
Requires Pillow (Python Imaging Library fork)
"""

import time

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import busio

# We need this for the pins, right now we're cheating and hard calling it.
import adafruit_blinka.board.raspberrypi.raspi_40pin as pins

# There are hard coded valid I2C pins sigh.
# busyio checks these before setting up an I2C, so they must be present for all busses.
import adafruit_blinka.microcontroller.bcm283x.pin
adafruit_blinka.microcontroller.bcm283x.pin.i2cPorts = (
    (5, pins.D22, pins.D18), (4, pins.D24, pins.D23), (3, pins.D27, pins.D17), (1, pins.SCL, pins.SDA), (0, pins.D1, pins.D0),   
)

def displayInit(oledDisplay):
    oledDisplay.fill(0)
    oledDisplay.show()
    return

def runCountdown(oledDisplay, displayNumber, sequenceStep):

    if sequenceStep < sequenceLast[displayNumber] :

        imageFile = 'images/pred' + str(sequenceStep + 1) + '-' + str(displayNumber + 1) + '.bmp'

        initialImage = Image.open(imageFile)
        # we need to rotate these -90 degrees and make sure they're single bit
        rotatedImage = initialImage.transpose(Image.ROTATE_270)
        twoBitImage = rotatedImage.convert("1")

        oledDisplay.image(twoBitImage)
    else :
        # blank the corresponding display 
        oledDisplay.fill(0)

    oledDisplay.show()
    return

busDictionary = { 
1 : { 'SDA': pins.SDA, 'SCL': pins.SCL }, 
3 : { 'SDA': pins.D17, 'SCL': pins.D27 },
4 : { 'SDA': pins.D23, 'SCL': pins.D24 },
5 : { 'SDA': pins.D18, 'SCL': pins.D22 }
}
busNumbers = [1, 3, 4, 5]

sequenceLast = [8, 6, 5, 3]

busList = [busio.I2C(busDictionary[x]['SCL'], busDictionary[x]['SDA']) for x in busNumbers]

displayList = [adafruit_ssd1306.SSD1306_I2C(128, 64, x, addr=0x3c) for x in busList]

totalAdvances = 0
sequenceNow = 0
delayInterval = 2

while totalAdvances < 10 :
    for i, display in enumerate(displayList):
        runCountdown(display, i, sequenceNow)
    totalAdvances += 1
    sequenceNow = totalAdvances % 9
    # note that for running indefinitely, we'll need a way to zero totalAdvances to prevent overflow (hence not a for loop)
    time.sleep(delayInterval)
    pass

