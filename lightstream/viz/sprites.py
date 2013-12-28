import pygame

from constants import *

class Block(pygame.sprite.Sprite):
	def __init__(self, color, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = 1
		self.rect.y = 1

	def move(self, x, y):
		self.rect.x = x
		self.rect.y = y

class PointSprite(pygame.sprite.Sprite):
	def __init__(self, x, y, r, g, b):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([SPRITE_SIZE, SPRITE_SIZE])
		self.rect = self.image.get_rect()
		self.set_color(r, g, b)
		self.set_position(x, y)

	def set_color(self, r, g, b):
		_r = int(255 * (r / LASER_CMAX_F))
		_g = int(255 * (g / LASER_CMAX_F))
		_b = int(255 * (b / LASER_CMAX_F))
		self.image.fill((_r, _g, _b))

	def set_position(self, x, y):
		_x = int(WINDOW_WIDTH/2 * (x / LASER_DMAX_F)) + WINDOW_WIDTH / 2
		_y = int(WINDOW_HEIGHT/2 * (y / LASER_DMAX_F)) + WINDOW_HEIGHT / 2
		self.rect.x = _x
		self.rect.y = _y

	def move(self, x, y):
		self.rect.x = x
		self.rect.y = y

