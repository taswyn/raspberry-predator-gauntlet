#!/usr/bin/python3.5

import time

import errno
from socket import error as socket_error

from multiprocessing.connection import Client

import os
import subprocess

import board
import digitalio

shutdownButton = digitalio.DigitalInOut(board.D21)
shutdownButton.direction = digitalio.Direction.INPUT
shutdownButton.pull = digitalio.Pull.UP

alreadyPressed = False

addressT = ('localhost', 8333)

#runForevvaarrrrr
while True :
    # if server is not running: ConnectionRefusedError: [Errno 111] Connection refused
    successfullySent = False
    if not shutdownButton.value :

        while not successfullySent and not alreadyPressed :
            try : 
                with Client(addressT) as connection :
                    connection.send(['shutdownPressed', None, 1])
                    successfullySent = True
            except socket_error as thisError :
                if thisError.errno != errno.ECONNREFUSED :
                    raise thisError
                print('server not running')
                # try to start the server
                pipeHolder = subprocess.Popen(['/usr/bin/python3.5', '/home/pi/raspberry-predator-gauntlet/predator-display-serv.py'])
                # wait for a little
                time.sleep(.5)
        alreadyPressed = True
        successfullySent = False

    if shutdownButton.value and alreadyPressed : 
        alreadyPressed = False

        while not successfullySent :
            try : 
                with Client(addressT) as connection :
                    connection.send(['shutdownReleased', None, 1])
                    successfullySent = True
            except socket_error as thisError :
                if thisError.errno != errno.ECONNREFUSED :
                    raise thisError
                print('server not running')
                # try to start the server
                pipeHolder = subprocess.Popen(['/usr/bin/python3.5', os.path.expanduser('~/raspberry-predator-gauntlet/predator-display-serv.py')])
                # wait for a little
                time.sleep(.5)
        successfullySent = False
    time.sleep(.1)