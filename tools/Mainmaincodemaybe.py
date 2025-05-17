from Joystickuseage import joystick_useage
from runnnnn_commmms import SerialComms
from MotorMovement import Startup
from convertCommandStringIntoSend import ConvertStuff  # Optional: remove if unused

class Main:
    def __init__(self):
        self.joystick = joystick_useage()
        self.motor = Startup()
        self.run_comms = SerialComms()
        self.convertToComms = ConvertStuff()  # Remove if not needed

        self.rawX = 0
        self.rawY = 0
        self.leftspeed = 0
        self.rightspeed = 0

    def main(self):
        print("System started. Listening to joystick input...")
        self.run_comms.sendComms("w odrv0.axis0.requested_state AXIS_STATE_CLOSED_LOOP_CONTROL")
        self.run_comms.sendComms("w odrv0.axis1.requested_state AXIS_STATE_CLOSED_LOOP_CONTROL")


        try:
            while True:
                self.rawX, self.rawY = self.joystick.gamepad_control_loop()
                self.leftspeed, self.rightspeed = self.motor.calculate_motor_speeds(self.rawY, self.rawX)

                # Handle LED or Trunk commands
                if self.joystick.LedState is not None:
                    self.run_comms.sendComms(self.joystick.LedState)
                    self.joystick.LedState = None

                if self.joystick.TrunkState is not None:
                    self.run_comms.sendComms(self.joystick.TrunkState)
                    self.joystick.TrunkState = None

                self.run_comms.receiveComms()  # Handle any responses
                if(self.leftspeed != 0):
                    self.motor.set_left_wheel_velocity(self.leftspeed)
                else:
                    self.run_comms.sendComms("v 0 0\n")

                if(self.rightspeed != 0):
                    self.motor.set_right_wheel_velocity(self.rightspeed)
                else:
                    self.run_comms.sendComms("v 1 0\n")

        except KeyboardInterrupt:
            print("\nShutting down...")
            self.motor.stop_motors()

        except Exception as e:
            print(f"Error in main loop: {e}")
            self.motor.stop_motors()

if __name__ == "__main__":
    robot_controller = Main()
    robot_controller.main()
