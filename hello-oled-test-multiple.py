"""
This is a basic test of two OLED SSD1306s connected via default I2c and GPIO to a Raspberry PI

Requires the CircuitPython library: adafruit-circuitpython-ssd1306 module
Requires Pillow (Python Imaging Library fork)
"""

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

def runDisplay(oledDisplay, displayNumber):
    oledDisplay.fill(0)
    oledDisplay.show()

    helloImage = Image.new('1', (oledDisplay.width, oledDisplay.height))

    drawObject = ImageDraw.Draw(helloImage)

    # white rectangle that nearly fills screen (2px border)
    drawObject.rectangle((2, 2, oledDisplay.width - 1, oledDisplay.height - 1), outline = 0, fill = 255)

    fontObject = ImageFont.load_default()

    drawText = "Hello OLED #" + str(displayNumber)

    (textWidth, textHeight) = fontObject.getsize(drawText)
    drawObject.text((oledDisplay.width / 2 - textWidth / 2, oledDisplay.height / 2 - textHeight / 2), drawText, font=fontObject, fill=0)

    oledDisplay.image(helloImage)
    oledDisplay.show()
    return

busDictionary = { 
1 : { 'SDA': pins.SDA, 'SCL': pins.SCL }, 
3 : { 'SDA': pins.D17, 'SCL': pins.D27 },
4 : { 'SDA': pins.D23, 'SCL': pins.D24 },
5 : { 'SDA': pins.D18, 'SCL': pins.D22 }
}
busNumbers = [1, 3, 4, 5]


busList = [busio.I2C(busDictionary[x]['SCL'], busDictionary[x]['SDA']) for x in busNumbers]


displayList = [adafruit_ssd1306.SSD1306_I2C(128, 64, x, addr=0x3c) for x in busList]

for i, display in enumerate(displayList):
    runDisplay(display, i)