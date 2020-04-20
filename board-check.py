import sys

from adafruit_blinka.agnostic import board_id, detector
import adafruit_platformdetect.constants.boards as ap_board

print(board_id)

print(detector.board.any_raspberry_pi_40_pin)

print(detector.board.any_raspberry_pi_cm)