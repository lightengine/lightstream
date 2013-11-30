from multiprocessing import Process, Queue, RLock

from net.macs import *
from find_dac import *
from oldlib import dac

from stream import QueueStream

class RepeaterProcess(Process):
	def __init__(self, macObj, queue=None):
		self._isRunning = False # XXX: A locked resource
		self._lock = RLock()
		self._macObj = macObj
		self._queueStream = QueueStream(queue=queue)

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

