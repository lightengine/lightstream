"""
Constants that make adjustment easier.
"""

LASER_CMAX = 65535 # Maximum color value (2^16-1)
LASER_DMAX = 32767 # TODO: Not certain if accurate (2^16/2-1)

LASER_CMAX_F = LASER_CMAX * 1.0
LASER_DMAX_F = LASER_DMAX * 1.0

COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)

WINDOW_WIDTH = int(640 * 1.5)
WINDOW_HEIGHT = int(480 * 1.5)

SPRITE_SIZE = 5

