import time

from multiprocessing.connection import Listener
from array import array

address = '/home/pi/raspberry-predator-gauntlet/connection-loc'
addressT = ('localhost', 8333)

with Listener(addressT) as server : 
    command = 'run'
    while command != 'finish' :
        with server.accept() as connection : 
            print('message received from', server.last_accepted)
            message = connection.recv()
            print(message)
            command = message[0]
        time.sleep(10)

# should we run the display from here directly?
# or should we create a lock and spawn a child process

# what if we get a message while we're in a given interior loop?
# from testing, this ends up working like a lightweight queue: 
# we pull connections off it FIFO even if they happened in the interim

# can we clear the queue down to the last one and discard the rest
# or do we need to process the full chain and then send a command when ready?

# note: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.connection.Connection.recv
# Connection.recv blocks until there is something to receive.