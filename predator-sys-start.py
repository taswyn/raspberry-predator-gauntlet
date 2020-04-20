#!/usr/bin/python3.5

import time

import errno
from socket import error as socket_error

from multiprocessing.connection import Client
from array import array

import subprocess
import os

address = '/home/pi/raspberry-predator-gauntlet/connection-loc'
addressT = ('localhost', 8333)

# if server is not running: ConnectionRefusedError: [Errno 111] Connection refused
successfullySent = False
while not successfullySent :
    try : 
        with Client(addressT) as connection :
            connection.send(['systemStart', None, 1])
            successfullySent = True
    except socket_error as thisError :
        if thisError.errno != errno.ECONNREFUSED :
            raise thisError
        print('server not running')
        # try to start the server
        pipeHolder = subprocess.Popen(['/usr/bin/python3.5', '/home/pi/raspberry-predator-gauntlet/predator-display-serv.py'])
        # wait for a little
        time.sleep(2)
