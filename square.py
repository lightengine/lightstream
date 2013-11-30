#!/usr/bin/env python

from oldlib import dac
from oldlib.common import *
from find_dac import find_dac_with_mac

import math
import itertools
import sys
import time

COLOR_R = CMAX
COLOR_G = CMAX
COLOR_B = CMAX

SIZE = 9000
XOFF = 0
YOFF = 0

def line_generator(pt1, pt2, backward=False, steps = 100):
	xdiff = pt1.x - pt2.x
	ydiff = pt1.y - pt2.y
	if not backward:
		for i in xrange(0, steps, 1):
			j = float(i)/steps
			x = pt1.x + (xdiff * j)
			y = pt1.y + (ydiff * j)
			yield (x, y, COLOR_R, COLOR_G, COLOR_B)

	else:
		for i in xrange(steps, 0, -1):
			j = float(i)/steps
			x = pt1.x + (xdiff * j)
			y = pt1.y + (ydiff * j)
			yield (x, y, COLOR_R, COLOR_G, COLOR_B)

class LinePointStream(object):

	def __init__(self, size=500, r=0, g=0, b=0, x=0, y=0):
		self.size = size
		self.r = r
		self.g = g
		self.b = b

		self.stream = self.produce()

		self.linePts = [
			(Point(0+x, 0+y), Point(0+x, size+y)),
			(Point(0+x, -size+y), Point(-size+x, -size+y)),
			(Point(size+x, -size+y), Point(size+x, -2*size+y)),
			(Point(size+x, 0+y), Point(2*size+x, 0+y))
		]

		self.curLineIdx = len(self.linePts)-1
		self.advanceLine()

	def advanceLine(self):
		self.curLineIdx = (self.curLineIdx+1) % len(self.linePts)
		self.curLine = line_generator(
							self.linePts[self.curLineIdx][0],
						    self.linePts[self.curLineIdx][1])

	def produce(self):
		while True:
			try:
				yield self.curLine.next()
			except:
				self.advanceLine()

			"""
			# Line out
			for i in xrange(0, steps, 1):
				j = float(i)/steps
				x = self.x1 + (xdiff * j)
				y = self.y1 + (ydiff * j)
				yield (x, y, self.r, self.g, self.b)

			# Line back in
			for i in xrange(0, steps, 1):
				j = float(i)/steps
				x = self.x2 - xdiff * j
				y = self.y2 - ydiff * j
				yield (x, y, self.r, self.g, self.b)
			"""

	def read(self, n):
		d = [self.stream.next() for i in xrange(n)]
		return d

while True:
	macaddr = sys.argv[1]
	print 'Going to find DAC w/ mac %s' % macaddr
	m = find_dac_with_mac(macaddr)
	try:
		d = dac.DAC(m)
		ps = LinePointStream(SIZE, x=XOFF, y=YOFF)
		print 'Play stream...'
		d.play_stream(ps)

	except KeyboardInterrupt:
		sys.exit()

	except Exception as e:
		# Hopefully the galvos aren't melting... 
		print "EXCEPTION"
		print e
		time.sleep(0.01)
		continue

