"""
Reimplements part of LobotServoController.cpp to
control LeArm via TTY. Enumerates the servos from 0 to 5
instead of 1 to 6 because I feel like it.
"""

import serial
from time import sleep

#from LobotServoController.h
FRAME_HEADER = 0x55 # firmware constant
CMD_SERVO_MOVE = 3 # firmware constant
BAUDRATE = 9600

TIMEOUT = 8

positions = [1500] * 6

def get_low_byte(i):
    return i % 256
def get_high_byte(i):
    return i >> 8

def move_to(servo, position, time):

    # validate position.
    # todo: check if the arm is capable of bending further than this
    if servo == 0: #claw
        position = min(max(position, 1500), 2500)
    else:
        position = min(max(position, 500), 2500)

    # from LobotServoController.cpp
    buffer = bytes([
        FRAME_HEADER,
        FRAME_HEADER,
        8,
        CMD_SERVO_MOVE,
        1,
        get_low_byte(time),
        get_high_byte(time),
        servo + 1,
        get_low_byte(position),
        get_high_byte(position)
    ])

    # we need permission to do this, so: sudo chmod 666 /dev/ttyUSB0
    with serial.Serial('/dev/ttyUSB0', BAUDRATE, timeout=TIMEOUT) as port:
        port.write(buffer)
    positions[servo] = position

def displace(servo, displacement, time):
    move_to(servo, positions[servo] + displacement, time)

def erect():
    for servo in range(6):
        move_to(servo, 1500, 1000)

# quick and dirty routine.
# a better way would be to set up frames of positions, with durations.
def dance():
    erect()
    for i in range(8):
        for servo in range(6):
            move_to(servo, 1900 + (i%2)*300, 400)
        sleep(0.4)
    erect()
