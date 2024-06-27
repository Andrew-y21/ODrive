#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math



wheelRadius = 0.2286
DimBetweenWheels = 0.762
# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
odrv0 = odrive.find_any()

# Calibrate motor and wait for it to finish
print("starting calibration...")
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while odrv0.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)
odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while odrv0.axis1.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

velo = 0
angle = 0
def inputt():
    while True:
        c = input("command:")
        if c == 'w':
            return 1
        elif c == 's':
            return 2
        elif c == 'a':
            return 3
        elif c == 'd':
            return 4
        else:
            return 0
        
def drive(velo, angle):
    vL= (2*velo-angle*DimBetweenWheels)/2*wheelRadius
    vR= -(2*velo+angle*DimBetweenWheels)/2*wheelRadius

    odrv0.axis0.controller.input_vel = vL
    odrv0.axis1.controller.input_vel = vR



def command_to_drive(command, velo, angle):
        
        if command == 1:
            velo += rate_of_increase
            
            return angle, velo
        elif command == 2:
            velo -= rate_of_increase
            
            return angle, velo
        elif command == 3:
            angle -= rate_of_increase
            
            return angle, velo
        elif command == 4:
            angle += rate_of_increase
            return angle, velo



        
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# To read a value, simply read the property
print("Bus voltage is " + str(odrv0.vbus_voltage) + "V")


#velo = input('velo')
#velo = float(velo)

#angle = input('angle')
#angle = float(angle)

#vL= (2*velo-angle*DimBetweenWheels)/2*wheelRadius
#vR= -(2*velo+angle*DimBetweenWheels)/2*wheelRadius

#odrv0.axis0.controller.input_vel = vL
#odrv0.axis1.controller.input_vel = vR

rate_of_increase = 5
help = 1

while help == 1:
    command = inputt()
    if command == 0:
        help = 0
        angle = 0
        velo = 0
        drive(velo, angle)
        break
    angle, velo = command_to_drive(command, velo, angle)
    print(angle, velo)
    drive(velo, angle)



        


    
        


    

# Or to change a value, just assign to the property
#odrv0.axis0.controller.input_pos = 3.14
#print("Position setpoint is " + str(odrv0.axis0.controller.pos_setpoint))

# And this is how function calls are done:
#for i in [1,2,3,4]:
#    print('voltage on GPIO{} is {} Volt'.format(i, odrv0.get_adc_voltage(i)))

# A sine wave to test
#t0 = time.monotonic()
#while True:
#    setpoint = 4.0 * math.sin((time.monotonic() - t0)*2)
#    print("goto " + str(int(setpoint)))
#    odrv0.axis0.controller.input_pos = setpoint
#    time.sleep(0.01)

# Some more things you can try:

# Write to a read-only property:
#odrv0.vbus_voltage = 11.0  # fails with `AttributeError: can't set attribute`

# Assign an incompatible value:
#odrv0.motor0.pos_setpoint = "I like trains"  # fails with `ValueError: could not convert string to float`
