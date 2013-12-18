#!/usr/bin/env python

import sys
import time
import pygame
import random
from threading import Thread, Lock

pygame.init()

COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

SPRITE_SIZE = 5

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

class PygameThread(Thread):
	def __init__(self):
		super(PygameThread, self).__init__()
		self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		self.lock = Lock()

		self.sprites = []
		self.spriteGroup = pygame.sprite.Group()

	def thread_add_sprite(self, x, y):
		sprite = Block(COLOR_RED, SPRITE_SIZE, SPRITE_SIZE)
		sprite.move(x, y)
		with self.lock:
			self.sprites.append(sprite)
			self.spriteGroup.add(sprite)

	def run(self):
		#a = Block(COLOR_RED, SPRITE_SIZE, SPRITE_SIZE)
		#self.sprites.add(a)
		while True:
			#a.rect.x = random.randint(0, WINDOW_WIDTH)
			#a.rect.y = random.randint(0, WINDOW_HEIGHT)
			#print a.rect.x, a.rect.y

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)

			x = random.randint(0, WINDOW_WIDTH)
			y = random.randint(0, WINDOW_HEIGHT)

			self.thread_add_sprite(x, y)

			with self.lock:
				self.spriteGroup.draw(self.window)

				if len(self.sprites) > 20:
					#print 'pop'
					sprite = self.sprites.pop(0)
					self.spriteGroup.remove(sprite)

			pygame.display.flip()
			self.window.fill(COLOR_BLACK)

def main():
	pt = PygameThread()
	pt.start()
	while True:
		time.sleep(10)

if __name__ == '__main__':
	main()

