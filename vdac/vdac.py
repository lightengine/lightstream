from multiprocessing import Process, Queue, RLock
from socket import *

#from broadcast import broadcast_get_client # TODO FIX IMPORT LIB NAMES
from broadcast import BroadcastThread
from etherdream import EtherdreamThread
from queue import SmallQueue

class VirtualDac(Process):
	"""
	Virtual Dac

	Emulates a hardware Etherdream DAC and interacts with a controlling
	laser projector program. It will capture data packets for external
	usage.
	"""

	def __init__(self, queue=None, host=''):
		super(VirtualDac, self).__init__()

		if not queue:
			#queue = SmallQueue()
			queue = Queue(maxsize=5)

		self._queue = queue
		self._is_running = False
		self._lock = RLock()

		self._host = host

	def get_queue(self):
		return self._queue

	def set_queue(self, queue):
		with self._lock: # TODO: Really bad lock semantics.
			self._queue = queue

	def run(self):
		"""
		Virtual dac mainloop.
		Broadcasts availability, accepts connections, queues
		inbound data packets. Self-healing, too.
		"""

		def get_client():
			# Listen for client connection
			s = socket(AF_INET, SOCK_STREAM)
			s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
			s.bind(('', 7765))
			s.listen(0.3)
			return s.accept() # return (csock, addr)

		with self._lock:
			self._is_running = True

		running = True

		while running:

			try:
				print 'Broadcasting... ASDF'
				bt = BroadcastThread(self._host)
				bt.start()
				csock, addr = get_client()
				bt.kill()

				print 'Got client', addr, csock

				EtherdreamThread(csock, addr, self._queue).main()

				print '...ended normally!?!'

			except Exception as e:
				print 'End broadcast...'
				print e

			with self._lock:
				running = self._is_running

	def end(self):
		with self._lock:
			self._is_running = False
