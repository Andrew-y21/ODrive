from gpiozero import OutputDevice
from time import sleep
import pygame

class Relays:
    def __init__(self):
    # Use GPIO pin 17 (you can change this)
        self.LinearUpPostive = OutputDevice(17, active_high=False, initial_value=False)
        self.LinearDownPostive = OutputDevice(22, active_high=False, initial_value=False)
        self.LinearUpNegitive = OutputDevice(27, active_high=False, initial_value=False)
        self.LinearDownNegitive = OutputDevice(23, active_high=False, initial_value=False)
        self.UnlockMotorRelays = OutputDevice(24, active_high=False, initial_value=False)
        #pygame.init()
        #pygame.joystick.init()
        self.joysticks = []
        self.LinearUpStatus = False
        self.LinearDownStatus = False




    def motorOn_Off(self, State):
        if State == True:
            self.UnlockMotorRelays.on()
        else:
            self.UnlockMotorRelays.off()

    #def trunkUp(self):
        
    
    """ 
    def getPresses(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Using joystick: {self.joystick.get_name()}")
        else:
            self.joystick = None
            print("No joystick detected!")

        running = True
        while running:
            pygame.event.pump()
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

            sleep(0.1) """

#    def moveBackUp(self):
        
    

#    def moveBackDown(self):








