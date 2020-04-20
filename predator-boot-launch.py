#!/usr/bin/python3.5

import subprocess

#Effectively fork these
startupPipeHolder = subprocess.Popen(['/usr/bin/python3.5', '/home/pi/raspberry-predator-gauntlet/predator-sys-start.py'])
buttonPipeHolder = subprocess.Popen(['/usr/bin/python3.5', '/home/pi/raspberry-predator-gauntlet/predator-shutdown-button.py'])