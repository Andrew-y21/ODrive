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
                self.motor.set_wheel_velocities(self.leftspeed, self.rightspeed)

        except KeyboardInterrupt:
            print("\nShutting down...")
            self.motor.stop_motors()

        except Exception as e:
            print(f"Error in main loop: {e}")
            self.motor.stop_motors()

if __name__ == "__main__":
    robot_controller = Main()
    robot_controller.main()
