import sys
import time
import pygame
import random
import struct
from threading import Thread, Lock
from multiprocessing import Queue as MQueue

pygame.init()

COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

LASER_CMAX = 65535 # MAX COLOR VALUE
LASER_DMAX = 30000 # TODO: Not accurate

LASER_CMAX_F = LASER_CMAX * 1.0
LASER_DMAX_F = LASER_DMAX * 1.0

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
		_x = int(WINDOW_WIDTH * (x / LASER_DMAX_F)) + WINDOW_WIDTH/2
		_y = int(WINDOW_HEIGHT * (y / LASER_DMAX_F)) + WINDOW_HEIGHT/2
		self.rect.x = _x
		self.rect.y = _y
		print _x, _y

	def move(self, x, y):
		self.rect.x = x
		self.rect.y = y

class PygameThread(Thread):
	def __init__(self, queue = None):
		super(PygameThread, self).__init__()
		self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		self.lock = Lock()

		self._queue = queue
		if not queue:
			self._queue = MQueue(maxsize=2)

		self.sprites = []
		self.spriteGroup = pygame.sprite.Group()

	def get_queue(self):
		return self._queue

	def set_queue(self, queue):
		with self.lock:
			self._queue = queue

	"""
	def thread_add_sprite(self, x, y):
		sprite = Block(COLOR_RED, SPRITE_SIZE, SPRITE_SIZE)
		sprite.move(x, y)
		with self.lock:
			self.sprites.append(sprite)
			self.spriteGroup.add(sprite)
	"""

	@staticmethod
	def _extract_points(data, divide=1):
		if type(divide) not in [int, float]:
			divide = 1
		if divide < 1:
			divide = 1

		# Points encoded in each packet
		numPoints = (len(data) - 3)/18
		off = 3
		for i in xrange(numPoints/divide):
			j = i*divide
			d = data[off+2:off+12]
			#off += 18
			off = 3 + (18 * i)

			x, y, r, g, b, = struct.unpack('<hhHHH', d)
			yield (x, y, r, g, b)

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

			#x = random.randint(0, WINDOW_WIDTH)
			#y = random.randint(0, WINDOW_HEIGHT)
			#self.thread_add_sprite(x, y)

			pygame.display.flip()
			self.window.fill(COLOR_BLACK)

			data = None
			if self._queue:
				with self.lock:
					try:
						data = self._queue.get_nowait()
					except:
						pass

			newPoints = []
			#sprites = []
			spriteGroup = pygame.sprite.Group()

			if data:
				for point in self._extract_points(data, divide=10):
					s = PointSprite(*point)

					"""
					self.sprites.append(s)
					self.spriteGroup.add(s)

					if len(self.sprites) > 100:
						sprite = self.sprites.pop(0)
						self.spriteGroup.remove(sprite)
					"""

					#sprites.append(s)
					spriteGroup.add(s)

			spriteGroup.draw(self.window)

			"""
			with self.lock:
				self.spriteGroup.draw(self.window)

				# Way worse performance...
				#while len(self.sprites) > 90:
				#	sprite = self.sprites.pop(0)
				#	self.spriteGroup.remove(sprite)
			"""



