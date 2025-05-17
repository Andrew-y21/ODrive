import pygame
import time

class joystick_useage:
    def __init__(self):
        self.LedState = None
        self.TrunkState = None    

        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        self.init_gamepad()

    def init_gamepad(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Using joystick: {self.joystick.get_name()}")
        else:
            self.joystick = None
            print("No joystick detected.")


    def map_joystick(self, value, deadzone=0.1):
        return 0 if abs(value) < deadzone else value

    def gamepad_control_loop(self):
        #print("Polling joystick...")
        # Handle events first
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(4):
                    self.TrunkState = "up"
                    print("up")
                if self.joystick.get_button(5):
                    self.TrunkState = "down"
                    print("down")
                if self.joystick.get_button(3):
                    self.LedState = "off"
                    print("off")
                if self.joystick.get_button(0):
                    self.LedState = "white"
                    print("white")
                if self.joystick.get_button(1):
                    self.LedState = "rainbow"
                    print("rain")
                if self.joystick.get_button(2):
                    self.LedState = "switch"
                    print("SWithc")

        # Read joystick axes
        if self.joystick:
            y = -self.map_joystick(self.joystick.get_axis(1))
            x = self.map_joystick(self.joystick.get_axis(0))
            if x > .2:
                print(x)
            if y > .2:
                print(y)
        else:
            x, y = 0, 0

        return x, y
