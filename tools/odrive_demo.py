#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math
import pygame





speed_increase = 2
wheelRadius = 0.2286
DimBetweenWheels = 0.762
# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
odrv0 = odrive.find_any()

# Calibrate motor and wait for it to finish
print("starting calibration...")
print("Bus voltage is " + str(odrv0.vbus_voltage) + "V")

odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

while odrv0.axis1.current_state != AXIS_STATE_IDLE:
   time.sleep(0.1)
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
#odrv0.axis1.requested_state = AXIS_STATE_MOTOR_CALIBRATION
#odrv0.axis1.requested_state = AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION
#odrv0.axis1.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
while odrv0.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)


odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

def drive(velocity, angle):
    #velocity *= 10
    vL= -(2*velocity-angle*DimBetweenWheels)/2*wheelRadius
    vR= (2*velocity+angle*DimBetweenWheels)/2*wheelRadius

    odrv0.axis1.controller.input_vel = vL
    odrv0.axis0.controller.input_vel = vR
# Initialize pygame
pygame.init()


# Initialize the joystick
pygame.joystick.init()

def calculate_angle_velocity(x, y):
    angle = math.atan2(x, -y) * (180 / math.pi)  # Convert radians to degrees
    velocity = math.sqrt(x**2 + y**2)  # Calculate the magnitude of the vector
    if(abs(x) <= .09 and abs(y) <= .09):
        angle = 0
        velocity = 0

    
    if( y > 0):
        velocity *= -1
    if(velocity < 0 and angle < 0):
        angle *= -1 
        angle -= 180
    elif(velocity < 0 and angle > 0):
        angle -= 180
        angle *= -1
    velocity *= speed_increase *2
    return angle, velocity

# Check for connected joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick initialized: {joystick.get_name()}")

    # Main loop
    try:
        while True:     
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    x = joystick.get_axis(0)  # Left stick x-axis
                    y = joystick.get_axis(1)  # Left stick y-axis
                    
                    # Calculate angle and velocity
                    angle, velocity = calculate_angle_velocity(x, y)

                    #                                                                              drive(velocity, angle)
                    vL= -(2*velocity-angle*DimBetweenWheels)/2*wheelRadius
                    vR= (2*velocity+angle*DimBetweenWheels)/2*wheelRadius

                    
                    odrv0.axis1.controller.input_vel = vL
                    
                    odrv0.axis0.controller.input_vel = vR
                    # Output the results
                    print(f"X: {x:.2f}, Y: {y:.2f} -> Angle: {angle:.2f} degrees, Velocity: {velocity:.2f}")
                
                elif event.type == pygame.JOYBUTTONDOWN:
                    button = event.button
                    
                    if(button == 0):
                        speed_increase += 1
                    elif(button == 3):
                        speed_increase -= 1
                        if(speed_increase == 0):
                            speed_increase = 1
                    else:
                        continue  

                    


                    

    except KeyboardInterrupt:
        print("Exiting...")
        odrv0.axis1.controller.input_vel = 0
        odrv0.axis0.controller.input_vel = 0
    finally:
        pygame.quit()


#velo = 0
#angle = 0
#def inputt():
#    while True:
#        c = input("command:")
#        if c == 'w':
#            return 1
#        elif c == 's':
#            return 2
#        elif c == 'a':
#            return 3
#        elif c == 'd':
#            return 4
#        else:
#            return 0
        
"""def drive(velocity, angle):
    velocity *= 10
    vL= (2*velocity-angle*DimBetweenWheels)/2*wheelRadius
    vR= (2*velocity+angle*DimBetweenWheels)/2*wheelRadius

    odrv0.axis1.controller.input_vel = vL
    odrv0.axis0.controller.input_vel = vR



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

"""

        
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
"""
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

"""

        


    
        


    

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
