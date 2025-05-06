from Joystickuseage import *
from runnnnn_commmms import *
from MotorMovement import *

class Main:
    def __init__(self):
        self.joystick = joystick_useage
        self.joystick.init_gamepad
        self.motor = Startup
        self.run_comms = SerialComms
        self.TrunkState = None
        self.LedColor = None
        self.rawX = 0
        self.rawY = 0
        self.leftspeed
        self.rightspeed




    def main(self):
       
       
       
       
       
       
        while True: # main loop
    
            self.LedColor, self.TrunkState, self.rawX, self.rawY = self.joystick.gamepad_control_loop()
            self.leftspeed, self.rightspeed = self.motor.calculate_motor_speeds(self.rawY, self.rawX)

            



