#!/usr/bin/env python3
from __future__ import print_function
import odrive
from odrive.enums import *
import time
import math
import pygame

# Constants
speed_increase = 2
wheelRadius = 0.2286  # Meters
DimBetweenWheels = 0.762  # Meters (width between wheels)

# Connect to ODrive
print("Finding an ODrive...")
odrv0 = odrive.find_any()

# Calibrate motors
print("Starting calibration...")
print(f"Bus voltage: {odrv0.vbus_voltage:.2f}V")

# Calibrate motor 1
odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while odrv0.axis1.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

# Calibrate motor 0
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while odrv0.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

# Set both axes to closed-loop control
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# Initialize Pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check for connected joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
    exit()

# Joystick connected
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Joystick initialized: {joystick.get_name()}")

def calculate_angle_velocity(x, y):
    """
    Calculate angle and velocity based on joystick x, y axes.
    """
    angle = math.atan2(x, -y) * (180 / math.pi)  # Radians to degrees
    velocity = math.sqrt(x ** 2 + y ** 2)  # Magnitude of the joystick input

    # Dead zone: prevent drift when joystick is near center
    if abs(x) < 0.1 and abs(y) < 0.1:
        angle = 0
        velocity = 0

    if y > 0:  # Reverse direction correction
        velocity *= -1

    # Angle adjustments for reverse movement
    if velocity < 0:
        if angle < 0:
            angle = -180 - angle
        else:
            angle = 180 - angle

    # Increase speed multiplier
    velocity *= speed_increase

    return angle, velocity

def drive(velocity, angle):
    """
    Calculate left and right motor velocities based on overall velocity and angle.
    """
    vL = -(2 * velocity - angle * DimBetweenWheels) / (2 * wheelRadius)
    vR = (2 * velocity + angle * DimBetweenWheels) / (2 * wheelRadius)

    # Apply calculated velocities to ODrive
    odrv0.axis1.controller.input_vel = vL
    odrv0.axis0.controller.input_vel = vR

# Main loop to control the motors based on joystick input
try:
    while True:
        # Get events from Pygame
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                # Read joystick axes
                x = joystick.get_axis(0)  # Left stick x-axis
                y = joystick.get_axis(1)  # Left stick y-axis

                # Calculate angle and velocity
                angle, velocity = calculate_angle_velocity(x, y)

                # Drive the motors based on the calculated angle and velocity
                drive(velocity, angle)

                # Output the joystick and calculated values
                print(f"X: {x:.2f}, Y: {y:.2f} -> Angle: {angle:.2f} degrees, Velocity: {velocity:.2f}")
            
            elif event.type == pygame.JOYBUTTONDOWN:
                # Handle joystick button presses
                button = event.button
                
                # Button 0 to increase speed, Button 3 to decrease speed
                if button == 0:
                    speed_increase += 1
                elif button == 3:
                    speed_increase = max(1, speed_increase - 1)  # Prevent going below 1

except KeyboardInterrupt:
    # Graceful exit on Ctrl+C
    print("Exiting...")
    odrv0.axis1.controller.input_vel = 0
    odrv0.axis0.controller.input_vel = 0

finally:
    # Quit Pygame
    pygame.quit()
