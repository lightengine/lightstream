import math
import time
import struct
from multiprocessing import Process, Queue, RLock

class QueueStream(object):

	def __init__(self, queue=None):
		if not queue:
			queue = Queue()

		self.called = False
		self._queue = queue
		self.stream = self.produce()

	def produce_circle(self):
		RESIZE_SPEED_INV = 200
		CMAX = 30000
		MAXRAD = 10260
		USERAD = MAXRAD
		LASER_POWER_DENOM = 1.0
		SAMPLE_PTS = 100 # 30 and below very damaging to galvos
		rad = int(USERAD)
		points = []
		for i in xrange(0, SAMPLE_PTS, 1):
			i = float(i) / SAMPLE_PTS * 2 * math.pi
			x = int(math.cos(i) * rad)
			y = int(math.sin(i) * rad)
			points.append((x, y, CMAX/LASER_POWER_DENOM,
						CMAX/LASER_POWER_DENOM,
						CMAX/LASER_POWER_DENOM))
		return points

	def produce_circle2(self):
		RESIZE_SPEED_INV = 200
		CMAX = 30000
		MAXRAD = 10260
		USERAD = MAXRAD/2
		LASER_POWER_DENOM = 1.0
		SAMPLE_PTS = 100 # 30 and below very damaging to galvos
		rad = int(USERAD)
		points = []
		for i in xrange(0, SAMPLE_PTS, 1):
			i = float(i) / SAMPLE_PTS * 2 * math.pi
			x = int(math.cos(i) * rad)
			y = int(math.sin(i) * rad)
			points.append((x, y, 0, CMAX, CMAX))

		return points

	def extract_points(self, buf):
		if len(buf) < 5:
			return False

		cmd, length = struct.unpack('<cH', str(buf[0:3]))
		data = buf[3:]

		if cmd != 'd':
			return False

		#print 'Data packets: %d' % length

		for i in xrange(length):
			j = i*18
			d = data[j:j+18]
			#print d

		return self.produce_circle2()

	def get_nowait(self):
		try:
			return self._queue.get_nowait()
		except Exception as e:
			return False

	def put_nowait(self, data):
		try:
			self._queue.put_nowait(data)
		except Exception as e:
			pass

	def produce(self):
		#print 'Streamer Produce...'
		count = 0
		while True:
			data = self.get_nowait()
			if data:
				# Points encoded in each packet
				numPoints = (len(data) - 3)/18
				off = 3
				for i in xrange(numPoints):

					d = data[off+2:off+12]
					off += 18

					x, y, r, g, b, = struct.unpack('<hhHHH', d)
					yield (x, y, r, g, b)

				count = 0
				#print 'qsize %d' % self._queue.qsize()
			else:
				count += 1
				#if count < 3:
				#	time.sleep(0.01)
				for pt in self.produce_circle():
					yield pt

				if count < 6 or \
					(count < 500 and count % 50 == 0) or \
					(count % 500 == 0):
						print 'queue empty %d' % count



	def read(self, n):
		d = [self.stream.next() for i in xrange(n)]
		return d


