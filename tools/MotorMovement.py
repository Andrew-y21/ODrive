import time
import math
import serial
from runnnnn_commmms import SerialComms


class Startup:
    def __init__(self, serial_port="/dev/serial0", baudrate=115200):
        self.wheelbase = 0.792
        self.wheel_radius = 0.2286
        self.encoder_cpr = 36
        self.left_direction = 1
        self.right_direction = -1
        self.max_speed = 4
        self.run_coms = SerialComms()

        #try:
        #    self.ser = serial.Serial(serial_port, baudrate, timeout=0.5)
        #except serial.SerialException as e:
        #    print(f"Serial error: {e}")
        #    self.ser = None

    def stop_motors(self):
        self.send_ascii_command("v 0 0\n")
        self.send_ascii_command("v 1 0\n")
        #self.run_coms.sendComms("v 0 0\n")
        #self.run_coms.sendComms("v 1 0\n")

    def send_ascii_command(self, command):
        #if not self.ser or not self.ser.is_open:
        #    #print("Serial not initialized.")
        #    return
        try:
            self.run_coms.sendComms(command)
            
            #self.ser.write(command.encode('utf-8'))
            #time.sleep(0.01)
            #response = self.ser.readline().decode('utf-8').strip()
            self.run_coms.receiveComms
                
        except Exception as e:
            print(f"UART Error: {e}")

    def set_left_wheel_velocity(self, left_vel):
        left_turns = (left_vel * self.left_direction) / (2 * math.pi * self.wheel_radius)
       

        self.send_ascii_command(f"v 0 {left_turns:.3f}\n")
        

    def set_right_wheel_velocity(self, right_vel):
        
        right_turns = (right_vel * self.right_direction) / (2 * math.pi * self.wheel_radius)

        
        self.send_ascii_command(f"v 1 {right_turns:.3f}\n")

    def map_joystick(self, value, deadzone=0.1):
        return 0 if abs(value) < deadzone else value

    def calculate_motor_speeds(self, y, x):
        left_speed = (y + x) * self.max_speed
        right_speed = (y - x) * self.max_speed

        max_val = max(abs(left_speed), abs(right_speed))
        if max_val > self.max_speed:
            left_speed *= self.max_speed / max_val
            right_speed *= self.max_speed / max_val

        return left_speed, right_speed
