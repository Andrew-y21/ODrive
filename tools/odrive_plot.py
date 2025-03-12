import odrive
from odrive.utils import start_liveplotter
#import matplotlib.pyplot as plt

# Find the ODrive
odrv0 = odrive.find_any()

# Run live plotter in the main thread
start_liveplotter(lambda: [odrv0.axis0.encoder.pos_estimate, odrv0.axis0.controller.pos_setpoint])
