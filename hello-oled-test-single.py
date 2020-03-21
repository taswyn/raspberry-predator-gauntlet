"""
This is a basic test of a single OLED SSD1306 connected via default I2c to a Raspberry PI

Requires the CircuitPython library: adafruit-circuitpython-ssd1306 module
Requires Pillow (Python Imaging Library fork)
"""

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

i2c = board.I2C()
oledDisplay = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

oledDisplay.fill(0)
oledDisplay.show()

helloImage = Image.new('1', (oledDisplay.width, oledDisplay.height))

drawObject = ImageDraw.Draw(helloImage)

# white rectangle that nearly fills screen (2px border)
drawObject.rectangle((2, 2, oledDisplay.width - 1, oledDisplay.height - 1), outline = 0, fill = 255)

fontObject = ImageFont.load_default()

drawText = "Hello OLED"

(textWidth, textHeight) = fontObject.getsize(drawText)
drawObject.text((oledDisplay.width / 2 - textWidth / 2, oledDisplay.height / 2 - textHeight / 2), drawText, font=fontObject, fill=0)

oledDisplay.image(helloImage)
oledDisplay.show()