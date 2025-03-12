import odrive
import time

try:
    from odrive.utils import dump_errors

    print("Finding ODrive...")
    odrv0 = odrive.find_any()
    print("Dumping errors...")
    dump_errors(odrv0, True)

    
    print("ODrive found. Saving configuration...")
    odrv0.save_configuration()
    print("Dumping errors...")
    dump_errors(odrv0, True)

    print("Configuration saved successfully.")
except Exception as e:
    print(f"Error: {e}")
