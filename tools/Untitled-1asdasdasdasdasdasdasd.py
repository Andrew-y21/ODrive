class DifferentialDriveController:
    def __init__(self):
        self.wheel_radius = 0.762  # Wheel radius in meters
        self.wheelbase = 0.5       # Distance between wheels in meters
        self.encoder_cpr = 4       # Encoder counts per revolution
        self.max_speed = 2.0       # Maximum linear speed in m/s
        self.min_speed = 0.1       # Minimum linear speed in m/s
        self.max_rotation_speed = 1.0  # Maximum rotational speed in rad/s
        self.x = 0                 # Robot's X position
        self.y = 0                 # Robot's Y position
        self.theta = 0             # Robot's heading (in radians)
        self.setup_odrive()

    def setup_odrive(self):
        print("Finding ODrive...")
        self.odrv0 = odrive.find_any()
        time.sleep(1)

        print("Configuring ODrive...")
        axes = [self.odrv0.axis0, self.odrv0.axis1]
        
        for axis in axes:
            axis.requested_state = AXIS_STATE_IDLE

            # Motor configuration
            axis.motor.config.current_lim = 20
            axis.motor.config.requested_current_range = 25
            axis.motor.config.calibration_current = 10
            axis.motor.config.pole_pairs = 2

            # Encoder configuration
            axis.encoder.config.mode = ENCODER_MODE_HALL
            axis.encoder.config.cpr = self.encoder_cpr
            axis.encoder.config.calib_scan_distance = 150

            # Controller configuration
            axis.controller.config.vel_limit = 10
            axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
            axis.controller.config.vel_ramp_rate = 0.5

        print("Starting motor calibration sequence...")
        # Calibrate motor 1
        self.odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while self.odrv0.axis1.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

        # Calibrate motor 0
        self.odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        while self.odrv0.axis0.current_state != AXIS_STATE_IDLE:
            time.sleep(0.1)

        print("Motor calibration complete. Setting closed-loop control...")
        # Set both axes to closed-loop control
        self.odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        self.odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        
        '''
        print("Saving configuration...")
        for attempt in range(3):  # Retry up to 3 times
            try:
                self.odrv0.save_configuration()
                time.sleep(2)
                print("Configuration saved successfully.")
                break
            except Exception as e:
                print(f"Error saving configuration: {e}")
                if attempt < 2:
                    print("Retrying...")
                    self.odrv0 = odrive.find_any()  # Reconnect to ODrive
                else:
                    print("Failed to save configuration after 3 attempts.")
                    raise e
        '''