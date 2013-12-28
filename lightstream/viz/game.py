import sys
import time
import pygame
import random
import struct

from threading import Thread, Lock
from multiprocessing import Queue as MQueue

from sprites import *
from constants import *

pygame.init()

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

	@staticmethod
	def _extract_points(data, divide=1):
		"""
		Extract point tuples from Etherdream packets.
		Use divide to skip points (evenly).
		"""
		if type(divide) not in [int, float]:
			divide = 1
		if divide < 1:
			divide = 1

		# Points encoded in each packet
		# (First 3: packet metadata, every 18 after: single point)
		numPoints = (len(data) - 3)/18
		off = 3
		for i in xrange(numPoints/divide):
			j = i*divide
			d = data[off+2:off+12]
			off = 3 + (18 * i)

			x, y, r, g, b, = struct.unpack('<hhHHH', d)
			yield (x, y, r, g, b)

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)

			pygame.display.flip()
			self.window.fill(COLOR_BLACK)

			data = None
			if self._queue:
				with self.lock:
					try:
						data = self._queue.get_nowait()
					except:
						pass

			spriteGroup = pygame.sprite.Group()

			if data:
				for point in self._extract_points(data, divide=2):
					s = PointSprite(*point)
					spriteGroup.add(s)

			spriteGroup.draw(self.window)

