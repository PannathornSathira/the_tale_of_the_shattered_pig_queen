SAVE_FILE_NAME = "saveFile.json"

WIDTH = 1280
HEIGHT = 720
MAX_FRAME_RATE = 60

TILE_SIZE = 32


# Character
CHARACTER_WIDTH = 55
CHARACTER_HEIGHT = 68

CHARACTER_MOVE_SPEED = 400
CAMERA_SCROLL_SPEED = 120

JUMP_FORCE = -800
GRAVITY = 2000

SKY = 35
GRASS = 33
GROUND_BOUNDARY = 43
GROUND = 53

GROUND_LEVEL_Y = 6 * TILE_SIZE * 3

# Platforms
NUM_ROW = 3
NUM_COL = 8

# Bullets
BULLET_SPEED = 500
BULLET_WIDTH = 5
BULLET_LENGTH = 10

# Beams
BEAM_HEIGHT = 200
BEAM_WIDTH = 1000
BEAM_SPEED = 1000

POTION_LEVELS = {
    "Health Potion": {"power": [0, 0.10, 0.15, 0.20, 0.25, 0.3]},
    "Damage Potion": {"power": [0, 1.05, 1.10, 1.15, 1.20, 1.25]},
    "Swiftness Potion": {"power": [0, 1.05, 1.10, 1.15, 1.20, 1.25]},
}
