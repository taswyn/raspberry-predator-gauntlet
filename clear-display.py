"""
Super basic clear single OLED display i2c

Requires the CircuitPython library: adafruit-circuitpython-ssd1306 module
"""

import board
import digitalio
import adafruit_ssd1306

i2c = board.I2C()
oledDisplay = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

oledDisplay.fill(0)
oledDisplay.show()
