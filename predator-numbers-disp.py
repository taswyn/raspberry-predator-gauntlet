"""
Requires the CircuitPython library: adafruit-circuitpython-ssd1306 module
Requires Pillow (Python Imaging Library fork)
"""

import time
import random
import math

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

screenOrientation = Image.ROTATE_270

def displayInit(oledDisplay):
    oledDisplay.fill(0)
    oledDisplay.show()
    return

def runCountdown(oledDisplay, displayNumber, sequenceStep) :

    if sequenceStep < sequenceLast[displayNumber] :

        imageFile = 'images/pred' + str(sequenceStep + 1) + '-' + str(displayNumber + 1) + '.bmp'

        initialImage = Image.open(imageFile)
        # we need to rotate these -90 degrees and make sure they're single bit
        rotatedImage = initialImage.transpose(screenOrientation)
        twoBitImage = rotatedImage.convert("1")

        oledDisplay.image(twoBitImage)
    else :
        # blank the corresponding display if past screen's sequence limit
        oledDisplay.fill(0)

    oledDisplay.show()
    return

def runExplosion(oledDisplays) :
    center = [math.floor(oledDisplays[0].width / 2), math.floor(oledDisplays[0].height / 2)]

    oledImages = [Image.new('1', (oledDisplay.width, oledDisplay.height)) for oledDisplay in oledDisplays]

    drawObjects = [ImageDraw.Draw(oledImage) for oledImage in oledImages]

    # this starts to get a little less than perfectly performant
    # consider using sprites/etc, or creating some random ones and then re-drawing with those
    for i in range(1, 15, 2) :
        for displayIndex, oledDisplay in enumerate(oledDisplays) :
            plotPoints = []
            for randomi in range (0, 30 * i * math.floor(i/1.5)) :
                x = random.randrange(-6*i, 6*i) + center[0]
                y = random.randrange(math.floor(-5*i), math.floor(5*i)) + center[1]
                plotPoints.append((x,y)) 
            
            drawObjects[displayIndex].point(plotPoints, fill=1)

            oledDisplay.image(oledImages[displayIndex])
            oledDisplay.show()
            
        # not an issue on Pi3B, but this should help keep timing consistent on faster systems
        time.sleep(.05)
    """    
    textLine1 = "GAME"
    textLine2 = "OVER"

    basicFont = ImageFont.truetype(font="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", size=60)

    # have to rotate the letters to fit the screen orientation!
    fontObject = ImageFont.TransposedFont(basicFont, orientation = screenOrientation)

    for displayIndex, oledDisplay in enumerate(oledDisplays) :
        (textWidth, textHeight) = fontObject.getsize(textLine1[displayIndex])
        drawObjects[displayIndex].text((center[0] + center[0] / 2 - textWidth / 2, center[1] - textHeight / 2), textLine1[displayIndex], font=fontObject, fill=0)
        oledDisplay.image(oledImages[displayIndex])
        oledDisplay.show()
        time.sleep(.05)

    for displayIndex, oledDisplay in enumerate(oledDisplays) :
        (textWidth, textHeight) = fontObject.getsize(textLine2[displayIndex])
        drawObjects[displayIndex].text((center[0] / 2 - textWidth / 2, center[1] - textHeight / 2), textLine2[displayIndex], font=fontObject, fill=0)
        oledDisplay.image(oledImages[displayIndex])
        oledDisplay.show()
        time.sleep(.05)
    """
    
    textLines = ["MAKE", "YOUR", "TIME"]

    basicFont = ImageFont.truetype(font="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", size=40)

    # have to rotate the letters to fit the screen orientation!
    fontObject = ImageFont.TransposedFont(basicFont, orientation = screenOrientation)

    for i, textLine in enumerate(textLines) : 
        for displayIndex, oledDisplay in enumerate(oledDisplays) :
            (textWidth, textHeight) = fontObject.getsize(textLine[displayIndex])
            drawObjects[displayIndex].text((center[0] + (oledDisplay.width / 3) * (1-i) - textWidth / 2, center[1] - textHeight / 2), textLine[displayIndex], font=fontObject, fill=0)
            oledDisplay.image(oledImages[displayIndex])
            oledDisplay.show()
            time.sleep(.05)
        time.sleep(1)

def runClock(oledDisplays) :
    # run the clock process
    # initialize displays
    for oledDisplay in oledDisplays :
        oledDisplay.fill(0)
        oledDisplay.show()

    while True : 
        for oledDisplay in oledDisplays :
            if random.randrange(0,15) > 11 :
                imageFile = 'images/pred-hex-' + '{:X}'.format(random.randrange(0, 15)) + '.bmp'

                initialImage = Image.open(imageFile)
                # we need to rotate these -90 degrees and make sure they're single bit
                rotatedImage = initialImage.transpose(screenOrientation)
                twoBitImage = rotatedImage.convert("1")

                oledDisplay.image(twoBitImage)
                oledDisplay.show()
        time.sleep(1)
    return

def killClock() : 
    # check for the clock process, kill it
    return

busDictionary = { 
1 : { 'SDA': pins.SDA, 'SCL': pins.SCL }, 
3 : { 'SDA': pins.D17, 'SCL': pins.D27 },
4 : { 'SDA': pins.D23, 'SCL': pins.D24 },
5 : { 'SDA': pins.D18, 'SCL': pins.D22 }
}

# can enumerate less than the total defined buses in busNumbers if desired
busNumbers = [1, 3, 4, 5]

# this is the highest count of drawn bitmaps for each screen
sequenceLast = [8, 6, 5, 3]

busList = [busio.I2C(busDictionary[x]['SCL'], busDictionary[x]['SDA']) for x in busNumbers]

displayList = [adafruit_ssd1306.SSD1306_I2C(128, 64, x, addr=0x3c) for x in busList]

totalAdvances = 0
sequenceNow = 0
delayInterval = 2

while (totalAdvances / 9) < 1 :
    for i, display in enumerate(displayList):
        runCountdown(display, i, sequenceNow)
    totalAdvances += 1
    sequenceNow = totalAdvances % 9
    # note that for running indefinitely, we'll need a way to zero totalAdvances to prevent overflow (hence not a for loop)
    time.sleep(delayInterval)
    pass

runExplosion(displayList)

time.sleep(10)

runClock(displayList)