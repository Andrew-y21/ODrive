import pygame
import time
import math
import serial

class Startup:
    def __init__(self, serial_port="/dev/serial0", baudrate=115200):
        self.wheelbase = 0.792
        self.wheel_radius = 0.2286
        self.encoder_cpr = 36
        self.left_direction = 1
        self.right_direction = -1
        self.max_speed = 4

        # Initialize Serial
        self.ser = serial.Serial(serial_port, baudrate, timeout=0.5)

        # Init pygame for gamepad
        pygame.init()
        self.joysticks = []
        pygame.joystick.init()
        self.init_gamepad()

    """def init_gamepad(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Using joystick: {self.joystick.get_name()}")
        else:
            self.joystick = None
            print("No joystick detected!")
"""
    def stop_motors(self):
        self.send_ascii_command("v 0 0\n")
        self.send_ascii_command("v 1 0\n")

    def send_ascii_command(self, command):
        try:
            self.ser.write(command.encode('utf-8'))
            time.sleep(0.01)
            response = self.ser.readline().decode('utf-8').strip()
            if response:
                print(f"ODrive response: {response}")
        except Exception as e:
            print(f"UART Error: {e}")

    def set_wheel_velocities(self, left_vel, right_vel):
        left_turns = (left_vel * self.left_direction) / (2 * math.pi * self.wheel_radius)
        right_turns = (right_vel * self.right_direction) / (2 * math.pi * self.wheel_radius)

        self.send_ascii_command(f"v 0 {left_turns:.3f}\n")
        self.send_ascii_command(f"v 1 {right_turns:.3f}\n")

    def map_joystick(self, value, deadzone=0.1):
        if abs(value) < deadzone:
            return 0
        return value

    def calculate_motor_speeds(self, y, x):
        left_speed = (y + x) * self.max_speed
        right_speed = (y - x) * self.max_speed
        max_val = max(abs(left_speed), abs(right_speed))
        if max_val > 10:
            left_speed /= max_val
            right_speed /= max_val
        return left_speed, right_speed

    """def gamepad_control_loop(self):
        running = True
        while running:
            pygame.event.pump()
            if self.joystick:
                y = -self.map_joystick(self.joystick.get_axis(1))
                x = self.map_joystick(self.joystick.get_axis(0))
                left_speed, right_speed = self.calculate_motor_speeds(y, x)
                self.set_wheel_velocities(left_speed, right_speed)
                time.sleep(0.1)
            else:
                print("No joystick connected")
                running = False
        pygame.quit()"""

"""def main():
    robot = Startup(serial_port="/dev/serial0")  # Change to your port
    robot.gamepad_control_loop()

if __name__ == "__main__":
    main()
"""