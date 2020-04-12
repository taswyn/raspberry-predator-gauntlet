"""
Requires the CircuitPython library: adafruit-circuitpython-ssd1306 module
Requires Pillow (Python Imaging Library fork)
"""

import time
import random
import math

import queue # for error handling of queue.Empty

from multiprocessing import Process, Queue
from multiprocessing.connection import Listener
from array import array

address = '/home/pi/raspberry-predator-gauntlet/connection-loc'
addressT = ('localhost', 8333)

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

# clear a specific display TODO collapse this and use clearDisplays instead
def displayInit(oledDisplay):
    oledDisplay.fill(0)
    oledDisplay.show()
    return

# clear all displays passed in
def clearDisplays(oledDisplays) :
    # initialize displays
    for oledDisplay in oledDisplays :
        oledDisplay.fill(0)
        oledDisplay.show()

def clockInterval(oledDisplays) :
    # run a single clock interval
    for oledDisplay in oledDisplays :
        if random.randrange(0,15) > 11 :
            imageFile = 'images/pred-hex-' + '{:X}'.format(random.randrange(0, 15)) + '.bmp'

            initialImage = Image.open(imageFile)
            # we need to rotate these -90 degrees and make sure they're single bit
            rotatedImage = initialImage.transpose(screenOrientation)
            twoBitImage = rotatedImage.convert("1")

            oledDisplay.image(twoBitImage)
            oledDisplay.show()
    return

# secondary process core loop (runs the screen)
def displayMain(processQueue):

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
  
    clearDisplays(displayList)
    displayMode = 'clock'
    timeInterval = 0

    while displayMode != 'finish' :

        # central queue dispatch and timer
        time.sleep(0.1)
        timeInterval += 1 # safe to keep accumulating this past 10 when outside of clock mode
        try :
            processMessage = processQueue.get(False) # non blocking
            displayMode = processMessage
            
        except queue.Empty : 
            pass # need to catch this but nothing to do
        
        if displayMode == 'clock' and timeInterval > 9 :
            clockInterval(displayList)
            timeInterval = 0

        if displayMode == 'clear' :
            clearDisplays(displayList)
            processMessage = processQueue.get() # blocking! (waits for a command to start up again)
            displayMode = processMessage

# primary process core loop (central communication dispatcher)
if __name__=='__main__':
    # set up the communications queue
    interProcessQueue = Queue()
    # start the NON BLOCKING child process to actually run the screen
    displayProcess = Process(target=displayMain, args=((interProcessQueue),))
    displayProcess.daemon = True
    displayProcess.start() # starts up in clock mode
    # start the primary loop that will listen for incoming commands and pass them to queue
    # note that THIS loop is BLOCKING
    with Listener(addressT) as server : 
        command = 'clock'
        while command != 'finish' :
            # message processing here
            interProcessQueue.put(command) # this takes care of sending an initial message if needed
            
            with server.accept() as connection : 
                print('message received from', server.last_accepted)
                message = connection.recv()
                print(message)
                command = message[0]
                
        interProcessQueue.put(command) # send the finish command, can process first if necessary

# should we run the display from here directly?
# or should we create a lock and spawn a child process

# what if we get a message while we're in a given interior loop?
# from testing, this ends up working like a lightweight queue: 
# we pull connections off it FIFO even if they happened in the interim

# can we clear the queue down to the last one and discard the rest
# or do we need to process the full chain and then send a command when ready?

# note: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.connection.Connection.recv
# Connection.recv blocks until there is something to receive.