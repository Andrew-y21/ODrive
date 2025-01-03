#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

def safe_stop(odrv):
    """Safely stop motors even if full initialization hasn't occurred"""
    try:
        if odrv and hasattr(odrv, 'axis0') and hasattr(odrv, 'axis1'):
            odrv.axis0.controller.input_vel = 0
            odrv.axis1.controller.input_vel = 0
    except Exception as e:
        print(f"Emergency stop failed: {e}")

class Startup:
    def __init__(self):
        # 9 inches = 0.2286 meters (radius)
        self.wheel_radius = 0.2286  # meters
        self.wheelbase = 0.762      # meters
        self.velo = 0
        self.x = 0
        self.y = 0
        self.theta = 0
        self.encoder_cpr = 36
        self.odrv0 = None
        
        # Track cumulative position for accurate distance
        self.left_pos_prev = 0
        self.right_pos_prev = 0
        self.total_distance = 0

        # Direction multipliers for each wheel (-1 to reverse direction)
        self.left_direction = -1   # Flip left wheel direction
        self.right_direction = 1   # Keep right wheel direction

        self.setup_odrive()
        
    def setup_odrive(self):
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

        self.odrv0.axis0.controller.config.vel_ramp_rate = 10.0
        self.odrv0.axis1.controller.config.vel_ramp_rate = 10.0
        
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

    def get_distance_moved(self):
        try:
            # Get current encoder positions (in motor rotations)
            left_pos = self.odrv0.axis0.encoder.pos_estimate
            right_pos = self.odrv0.axis1.encoder.pos_estimate
            
            # Convert motor positions to wheel positions by dividing by the gear ratio
            left_wheel_pos = left_pos / 6
            right_wheel_pos = right_pos / 6

            # Calculate position changes
            left_delta = (left_wheel_pos - self.left_pos_prev) * self.left_direction
            right_delta = (right_wheel_pos - self.right_pos_prev) * self.right_direction
            
            # Update previous positions
            self.left_pos_prev = left_wheel_pos
            self.right_pos_prev = right_wheel_pos
            
            # Calculate distance moved (average of both wheels)
            distance = ((left_delta + right_delta) / 2) * (2 * math.pi * self.wheel_radius)
            
            return distance
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return 0

    def move_to_heading_and_distance(self, target_heading_deg, target_distance):
        try:
            # Reset total distance at start of movement
            self.total_distance = 0
            
            target_heading = math.radians(target_heading_deg)
            print(f"Rotating to heading {target_heading_deg} degrees...")
            rotation_speed = 2

            # Rotation phase
            while abs(self.normalize_angle(target_heading - self.theta)) > 0.05:
                angle_diff = self.normalize_angle(target_heading - self.theta)
                if angle_diff > 0:
                    self.set_wheel_velocities(rotation_speed, -rotation_speed)
                else:
                    self.set_wheel_velocities(-rotation_speed, rotation_speed)
                self.update_position()
                time.sleep(0.05)

            self.stop_motors()
            time.sleep(0.1)
            print("Heading achieved")
            
            # Reset encoder positions before starting forward movement
            self.left_pos_prev = self.odrv0.axis0.encoder.pos_estimate
            self.right_pos_prev = self.odrv0.axis1.encoder.pos_estimate
            
            # Forward movement phase
            print(f"Moving {target_distance} meters...")
            forward_speed = 2
            direction = 1 if target_distance > 0 else -1
            
            while abs(self.total_distance) < abs(target_distance):
                speed = forward_speed * direction
                self.set_wheel_velocities(speed, speed)
                
                # Update distance moved
                distance_increment = self.get_distance_moved()
                self.total_distance += distance_increment
                
                # Print current distance
                print(f"Distance moved: {abs(self.total_distance):.2f} meters")
                
                time.sleep(0.05)

            self.stop_motors()
            print("Movement complete")
            print(f"Total distance moved: {abs(self.total_distance):.2f} meters")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            self.stop_motors()
        except Exception as e:
            print(f"Error during movement: {e}")
            self.stop_motors()

    def update_position(self):
        try:
            # Get current encoder positions (in motor rotations)
            left_pos = self.odrv0.axis0.encoder.pos_estimate
            right_pos = self.odrv0.axis1.encoder.pos_estimate

            # Convert motor positions to wheel positions by dividing by the gear ratio
            left_wheel_pos = left_pos / 6
            right_wheel_pos = right_pos / 6

            # Apply direction multipliers to position calculations
            left_distance = (left_wheel_pos * self.left_direction) * (2 * math.pi * self.wheel_radius) / self.encoder_cpr
            right_distance = (right_wheel_pos * self.right_direction) * (2 * math.pi * self.wheel_radius) / self.encoder_cpr

            distance = (left_distance + right_distance) / 2
            self.theta += (right_distance - left_distance) / self.wheelbase

            self.x += distance * math.cos(self.theta)
            self.y += distance * math.sin(self.theta)
        except Exception as e:
            print(f"Error updating position: {e}")



    @staticmethod
    def normalize_angle(angle):
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle

def main():
    controller = None
    try:
        controller = Startup()

        while True:
            heading = float(input("Enter target heading (degrees): "))
            distance = float(input("Enter target distance (meters): "))
            controller.move_to_heading_and_distance(heading, distance)

            if input("Move again? (y/n): ").lower() != 'y':
                break

    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if controller and hasattr(controller, 'odrv0'):
            controller.stop_motors()
        elif controller:
            safe_stop(controller.odrv0)

if __name__ == "__main__":
    main()