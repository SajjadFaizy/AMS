from config import TIME_STEP

def setup_devices(epuck):
    """
    Configure the robot's devices and return them as a dictionary.
    """
    # Proximity Sensors
    ps = []
    for name in [f"ps{i}" for i in range(8)]: # List with names of ps (ps0, ..., ps7)
        sensor = epuck.getDevice(name)
        sensor.enable(TIME_STEP)
        ps.append(sensor)

    # GPS
    gps = epuck.getDevice("gps")
    gps.enable(TIME_STEP)

    # Compass
    compass = epuck.getDevice("compass")
    compass.enable(TIME_STEP)

    # Motors
    left_motor = epuck.getDevice('left wheel motor')
    right_motor = epuck.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    # Return all devices as a dictionary
    return {
        'ps': ps,
        'gps': gps,
        'compass': compass,
        'left_motor': left_motor,
        'right_motor': right_motor
    }