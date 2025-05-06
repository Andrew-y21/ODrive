import pygame
import math
import time 

class joystick_useage:
    def __init__(self):

        self.LedState = None
        self.TrunkState = None    

        pygame.init()
        self.joysticks = []
        pygame.joystick.init()
        self.init_gamepad()
        


    def init_gamepad(self):
            if pygame.joystick.get_count() > 0:
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                print(f"Using joystick: {self.joystick.get_name()}")
            else:
                self.joystick = None
                print("No joystick detected!")


    def map_joystick(self, value, deadzone=0.1):
        if abs(value) < deadzone:
            return 0
        return value
    

   

    def gamepad_control_loop(self):

        #LedState = None
        #TrunkState = None    
        running = True
        while running:
            pygame.event.pump()

            # Read joystick axes
            if self.joystick:
                y = -self.map_joystick(self.joystick.get_axis(1))
                x = self.map_joystick(self.joystick.get_axis(0))
                time.sleep(0.1)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if self.joystick.get_button(11):
                        self.TrunkState = "up"

                    if self.joystick.get_button(12):
                        self.TrunkState = "down"

                    if self.joystick.get_button(3):
                        self.LedState = "off"

                    if self.joystick.get_button(0):
                        self.LedState = "white"

                    if self.joystick.get_button(1):
                        self.LedState = "rainbow"
                    
                    if self.joystick.get_button(2):
                        self.LedState = "swtich"

        return x, y





        pygame.quit()


