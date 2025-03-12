import pygame
import math

# Initialize pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Function to calculate the angle and velocity from x, y positions
def calculate_angle_velocity(x, y):
    angle = math.atan2(x, -y) * (180 / math.pi)  # Convert radians to degrees
    velocity = math.sqrt(x**2 + y**2)  # Calculate the magnitude of the vector
    if(abs(x) <= .09 and abs(y) <= .09):
        angle = 0
        velocity = 0

    if( y > 0):
        velocity *= -1
    if(velocity < 0 and angle < 0):
        angle *= -1 
        angle -= 180
    elif(velocity < 0 and angle > 0):
        angle -= 180
        angle *= -1
    return angle, velocity

# Check for connected joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick connected")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick initialized: {joystick.get_name()}")

    # Main loop
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    x = joystick.get_axis(0)  # Left stick x-axis
                    y = joystick.get_axis(1)  # Left stick y-axis

                    # Calculate angle and velocity
                    angle, velocity = calculate_angle_velocity(x, y)

                    # Output the results
                    print(f"X: {x:.2f}, Y: {y:.2f} -> Angle: {angle:.2f} degrees, Velocity: {velocity:.2f}")


                    

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()
