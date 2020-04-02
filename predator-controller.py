import time

from multiprocessing.connection import Client
from array import array

address = '/home/pi/raspberry-predator-gauntlet/connection-loc'
addressT = ('localhost', 8333)

# if server is not running: ConnectionRefusedError: [Errno 111] Connection refused
with Client(addressT) as connection :
    connection.send(['test', None, 1])

# what if the server stalls out?
time.sleep(2)

with Client(addressT) as connection :
    connection.send(['test', None, 1])

time.sleep(11)

with Client(addressT) as connection :
    connection.send(['finish', None, 1])
