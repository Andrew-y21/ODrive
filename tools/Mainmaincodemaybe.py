from Joystickuseage import *
from runnnnn_commmms import *
from MotorMovement import *
from convertCommandStringIntoSend import *

class Main:
    def __init__(self):
        self.joystick = joystick_useage
        self.joystick.init_gamepad
        self.motor = Startup
        self.run_comms = SerialComms
        self.convertToComms = ConvertStuff
        #self.TrunkState = None
        #self.LedColor = None
        self.rawX = 0
        self.rawY = 0
        self.leftspeed
        self.rightspeed





    def main(self):
       
       
       
       
       
       
        while True: # main loop
    
            self.rawX, self.rawY = self.joystick.gamepad_control_loop()
            self.leftspeed, self.rightspeed = self.motor.calculate_motor_speeds(self, self.rawY, self.rawX)

            if (self.joystick().LedState != None or self.joystick().TrunkState != None):

                self.run_comms(self.joystick().LedState)
                self.run_comms(self.joystick().TrunkState)

                self.run_comms.reciveComms()

                self.joystick().LedState = None
                self.joystick().TrunkState = None
        
            self.motor.set_wheel_velocities(self, self.leftspeed, self.rightspeed)

            

            
















if __name__ == "__main__":
    Main()

                

















