TIME_STEP = 64  # [ms] - Refresh rate main loop


# 📡 Sensors
OBSTACLE_THRESHOLD = 80  # (0-4095) Reflected IR - Threshold obstacle detection
OBSTACLE_DANGER_THRESHOLD = 150  # (0-4095) Reflected IR - Threshold obstacle avoidance

# 🧭 Navigation
MAP_NAME = "farm_new"
MAP_GRID_RESOLUTION = 0.05 # [m] Difference real to matrix coordinates
DISTANCE_THRESHOLD = 0.01  # [m] Target arrival threshold
HEADING_ERROR_THRESHOLD = 0.05  # [rad] Heading correction threshold

# Avoidance System
AVOIDANCE_DISTANCE = 0.2  # [m]
AVOIDANCE_MAX_TRIES = 2
AVOIDANCE_DELETE_WP_QTY = 3
AVOIDANCE_DELETE_THRESHOLD = MAP_GRID_RESOLUTION * 4

# 🚦 Navigation States
STATE_STOP = 0
STATE_GPS = 1
STATE_OBSTACLE_LEFT = 2
STATE_OBSTACLE_RIGHT = 3

# 🤖 Robot
WHEEL_RADIUS = 0.0205 # [m]
MAX_SPEED_ENGINES = 5  # [rad/s] - Max Wheel speed

# 🖥️ Monitoring Panel
GUI_SETTINGS = {
    "TITLE": "Variable Monitor - Webots",
    "SIZE": "1240x800",  # Window size
    "BG_COLOR": "#f0f0f0",  # Background color
    "TITLE_FONT": ("Arial", 12, "bold"),  # Font for titles
    "VALUE_FONT": ("Arial", 18, "bold"),  # Font for values
    "FG_COLOR": "#333333"  # Foreground text color
}