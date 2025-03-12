#!/usr/bin/env python3
import odrive
from odrive.enums import *
import time
import math

class DifferentialDriveController:
    def __init__(self):
        self.wheel_radius = 0.762  # Wheel radius in meters
        self.wheelbase = 0.5       # Distance between wheels in meters
        self.encoder_cpr = 4       # Encoder counts per revolution
        self.max_speed = 2.0       # Maximum linear speed in m/s
        self.min_speed = 0.1       # Minimum linear speed in m/s
        self.max_rotation_speed = 1.0  # Maximum rotational speed in rad/s
        self.x = 0                 # Robot's X position
        self.y = 0                 # Robot's Y position
        self.theta = 0             # Robot's heading (in radians)
        self.setup_odrive()

    def setup_odrive(self):
        print("Finding ODrive...")
        self.odrv0 = odrive.find_any()
        time.sleep(1)

        print("Configuring ODrive...")
        axes = [self.odrv0.axis0, self.odrv0.axis1]
        
        for axis in axes:
            axis.requested_state = AXIS_STATE_IDLE

            # Motor configuration
            axis.motor.config.current_lim = 20
            axis.motor.config.requested_current_range = 25
            axis.motor.config.calibration_current = 10
            axis.motor.config.pole_pairs = 2

            # Encoder configuration
            axis.encoder.config.mode = ENCODER_MODE_HALL
            axis.encoder.config.cpr = self.encoder_cpr
            axis.encoder.config.calib_scan_distance = 150

            # Controller configuration
            axis.controller.config.vel_limit = 10
            axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
            axis.controller.config.vel_ramp_rate = 0.5

        print("Starting motor calibration sequence...")
        # Calibrate motor 1
        self.odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while self.odrv0.axis1.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

        # Calibrate motor 0
        self.odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while self.odrv0.axis0.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

        print("Motor calibration complete. Setting closed-loop control...")
        # Set both axes to closed-loop control
        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        
    def set_wheel_velocities(self, left_vel, right_vel):
        try:
            left_turns = left_vel / (2 * math.pi * self.wheel_radius)
            right_turns = right_vel / (2 * math.pi * self.wheel_radius)

            self.odrv0.axis0.controller.input_vel = left_turns
            self.odrv0.axis1.controller.input_vel = -right_turns
        except Exception as e:
            print(f"Error setting velocities: {e}")
            self.emergency_stop()

    def emergency_stop(self):
        try:
            self.odrv0.axis0.controller.input_vel = 0
            self.odrv0.axis1.controller.input_vel = 0
        except Exception as e:
            print(f"Emergency stop failed: {e}")

    def move_to_heading_and_distance(self, target_heading_deg, target_distance):
        try:
            target_heading = math.radians(target_heading_deg)
            print(f"Rotating to heading {target_heading_deg} degrees...")
            rotation_speed = 0.5

            # Rotate to the target heading
            while abs(self.normalize_angle(target_heading - self.theta)) > 0.05:
                if self.normalize_angle(target_heading - self.theta) > 0:
                    self.set_wheel_velocities(rotation_speed, -rotation_speed)
                else:
                    self.set_wheel_velocities(-rotation_speed, rotation_speed)
                self.update_position()
                time.sleep(0.1)

            self.set_wheel_velocities(0, 0)
            print("Heading achieved")

            print(f"Moving {target_distance} meters...")
            forward_speed = 0.5
            direction = 1 if target_distance > 0 else -1
            start_time = time.time()

            while time.time() - start_time < abs(target_distance / forward_speed):
                self.set_wheel_velocities(forward_speed * direction, forward_speed * direction)
                self.update_position()
                time.sleep(0.1)

            self.set_wheel_velocities(0, 0)
            print("Movement complete")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            self.emergency_stop()
        except Exception as e:
            print(f"Error during movement: {e}")
            self.emergency_stop()

    def update_position(self):
        try:
            left_pos = self.odrv0.axis0.encoder.pos_estimate
            right_pos = self.odrv0.axis1.encoder.pos_estimate

            left_distance = left_pos * (2 * math.pi * self.wheel_radius) / self.encoder_cpr
            right_distance = right_pos * (2 * math.pi * self.wheel_radius) / self.encoder_cpr

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
    try:
        controller = DifferentialDriveController()

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
        try:
            controller.emergency_stop()
        except:
            pass

if __name__ == "__main__":
    main()
