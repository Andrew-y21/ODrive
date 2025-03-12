from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math
import pygame

class Startup:
    def __init__(self):
        self.wheelbase = 0.792
        self.wheel_radius = 0.2286
        self.velo = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.encoder_cpr = 36
        self.odrv0 = None


        self.left_pos_prev = 0
        self.right_pos_prev = 0

        self.left_direction = -1   # Flip left wheel direction
        self.right_direction = 1   # Keep right wheel direction

        pygame.init()

        self.joysticks = []
        pygame.joystick.init()

    def startup_odrive(self):
        print("finding an odrive...")
        self.odrv0 = odrive.find_any()
        
        # Reset both axes
        self.odrv0.axis0.requested_state = AXIS_STATE_IDLE
        self.odrv0.axis1.requested_state = AXIS_STATE_IDLE
        time.sleep(0.01)
        
        # Configure both axes
        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        time.sleep(0.01)


        self.odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        self.odrv0.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
        
        # Initialize previous positions
        self.left_pos_prev = self.odrv0.axis0.encoder.pos_estimate
        self.right_pos_prev = self.odrv0.axis1.encoder.pos_estimate

        print("Bus voltage is " + str(self.odrv0.vbus_voltage) + "V")

    def stop_motors(self):
        """Stop both motors"""
        try:
            if self.odrv0:
                self.odrv0.axis0.controller.input_vel = 0
                self.odrv0.axis1.controller.input_vel = 0
                time.sleep(0.01)
        except Exception as e:
            print(f"Stop motors failed: {e}")

    def set_wheel_velocities(self, left_vel, right_vel):
        try:
            # Convert linear velocity to turns per second and apply direction multipliers
            left_turns = (left_vel * self.left_direction) / (2 * math.pi * self.wheel_radius)
            right_turns = (right_vel * self.right_direction) / (2 * math.pi * self.wheel_radius)

            # Set velocities simultaneously
            self.odrv0.axis0.controller.input_vel = left_turns
            self.odrv0.axis1.controller.input_vel = right_turns

            # Small delay to allow velocity to update
            time.sleep(0.01)
            
            # Get actual velocities
            actual_left_vel = self.odrv0.axis0.encoder.vel_estimate
            actual_right_vel = self.odrv0.axis1.encoder.vel_estimate

            # Convert turns/s back to m/s for meaningful feedback
            actual_left_mps = actual_left_vel * (2 * math.pi * self.wheel_radius) * self.left_direction
            actual_right_mps = actual_right_vel * (2 * math.pi * self.wheel_radius) * self.right_direction
            
            # Print actual velocities and target velocities
            print(f"Left wheel - Target: {left_vel:.2f} m/s, Actual: {actual_left_mps:.2f} m/s")
            print(f"Right wheel - Target: {right_vel:.2f} m/s, Actual: {actual_right_mps:.2f} m/s")
            
        except Exception as e:
            print(f"Error setting velocities: {e}")
            self.stop_motors()

def main():
    self = Startup()

   


    for event in pygame.event.get():
        if event.type == pygame.JOYDEVICEADDED:
            joy = pygame.joystick.Joystick(event.device_index)
            self.joysticks.append(joy)

    for joystick in self.joysticks:
        horiz_move = pygame.JOYAXISMOTION
        