VIDEO_PATH = "videos/D01_20260311055957.mp4"

FRAME_INTERVAL = 1  # seconds between sampled frames

LOG_INTERVAL = 10  # seconds between log lines when no people are detected

# Each color maps to a list of (lower, upper) HSV tuples.
# Multiple ranges allow colors that wrap around hue (e.g. red spans 0-10 and 160-180).
HSV_COLORS = {
    "red": [
        ((0, 100, 100), (10, 255, 255)),
        ((160, 100, 100), (180, 255, 255)),
    ],
    "blue": [
        ((100, 100, 100), (130, 255, 255)),
    ],
    "yellow": [
        ((20, 100, 100), (35, 255, 255)),
    ],
    "green": [
        ((35, 40, 40), (85, 255, 255)),
    ],
    "orange": [
        ((10, 100, 100), (20, 255, 255)),
    ],
}

TARGET_COLOR = "green"

COLOR_THRESHOLD = 0.15  # minimum ratio of matching pixels

LOG_FILE = "output/logs.txt"

SHOW_DEBUG = False
