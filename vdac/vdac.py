from multiprocessing import Process, Queue, RLock
from socket import *

#from broadcast import broadcast_get_client # TODO FIX IMPORT LIB NAMES
from broadcast import BroadcastThread
from etherdream import EtherdreamThread
from temp import *

class VirtualDac(Process):
	"""
	Virtual Dac

	Emulates a hardware Etherdream DAC and interacts with a controlling
	laser projector program. It will capture data packets for external
	usage.
	"""

	def __init__(self, queue=None):
		super(VirtualDac, self).__init__()

		if not queue:
			queue = Queue()

		self._queue = queue
		self._is_running = False
		self._lock = RLock()

	def get_queue(self):
		return self._queue

	def set_queue(self, queue):
		with self._lock: # TODO: Really bad lock semantics.
			self._queue = queue

	def run(self):
		with self._lock:
			self._is_running = True

		running = True

		while running:
			bt = BroadcastThread()

			try:
				print 'Broadcasting...'

				bt.start()

				# Listen for client connection
				s = socket(AF_INET, SOCK_STREAM)
				s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
				s.bind(('localhost', 7765))
				s.listen(3)

				(csock, addr) = s.accept()

				bt.kill()

				#return (csock, addr)
				#csock, addr = broadcast_get_client()

				print 'Got client', addr, csock

				cs = EtherdreamThread(csock, addr, self._queue)
				cs.communicate()

			except Exception as e:
				print e
				raise e
				pass

			with self._lock:
				running = self._is_running

	def end(self):
		with self._lock:
			self._is_running = False
