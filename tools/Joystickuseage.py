import pygame
import math
import time 

class joystick_useage:
    def __init__(self):

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
        
        
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
                elif event.type == pygame.JOYBUTTONDOWN:
                    if self.joystick.get_button(0):
                        self.LinearDown.off()
                        self.LinearUp.on()
                        print("Up relay on")

                    elif self.joystick.get_button(1):
                        self.LinearUp.off()
                        self.LinearDown.on()
                        print("Down relay on")

                elif event.type == pygame.JOYBUTTONUP:
                    self.LinearUp.off()
                    self.LinearDown.off()




        pygame.quit()


