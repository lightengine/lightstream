#!/usr/bin/env python

import math
import itertools
import sys
import time

CMAX = 30000
MAXRAD = 10260
USERAD = MAXRAD

LASER_POWER_DENOM = 1.0
SAMPLE_PTS = 100 # 30 and below very damaging to galvos


class CircleStream(object):
	def produce(self):
		RESIZE_SPEED_INV = 200
		while True:
			rad = int(USERAD)
			for i in xrange(0, SAMPLE_PTS, 1):
				i = float(i) / SAMPLE_PTS * 2 * math.pi
				x = int(math.cos(i) * rad)
				y = int(math.sin(i) * rad)
				yield (x, y, CMAX/LASER_POWER_DENOM,
							CMAX/LASER_POWER_DENOM,
							CMAX/LASER_POWER_DENOM)

	def __init__(self):
		self.called = False
		self.stream = self.produce()

	def read(self, n):
		d = [self.stream.next() for i in xrange(n)]
		return d

