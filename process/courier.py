import math
from multiprocessing import Process, Queue, RLock

from macs import *
from find_dac import *
from oldlib import dac

class QueueStream(object):
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
		while True:
			data = self.get_nowait()

			if not data:
				for pt in self.produce_circle():
					yield pt
				continue

			if data:
				for pt in self.produce_circle2():
					yield pt
				continue

			#print 'Data:'
			cmd, length = struct.unpack("<cH", data)
			#print cmd, length


	def __init__(self):
		self.called = False
		self._queue = Queue()
		self.stream = self.produce()

	def read(self, n):
		d = [self.stream.next() for i in xrange(n)]
		return d

class RepeaterProcess(Process):
	def __init__(self, macObj):
		self._isRunning = False # XXX: A locked resource
		self._lock = RLock()
		self._macObj = macObj
		self._queueStream = QueueStream()

		super(RepeaterProcess, self).__init__()

	def getQueue(self):
		return self._queueStream._queue # TODO FIXME BAD

	def run(self):
		with self._lock:
			self._isRunning = True

		running = True

		while running:
			try:
				addr = find_dac_with_mac(self._macObj)

				"""
				print '\n    - '.join([
					'Connecting to:',
					'%s (mac)' % self._macObj.macStr,
					'%s (addr)' % addr
				])
				"""

				d = dac.DAC(addr)
				d.play_stream(self._queueStream)

			except Exception as e:
				#print 'Exception'
				#print e
				pass

			with self._lock:
				running = self._isRunning

	def put_nowait(self, data):
		self._queueStream.put_nowait(data)

