import time
import threading
from socket import *

from packets import BroadcastPacket

class BroadcastThread(threading.Thread):

	# Host options: '', 255.255.255.255, 'localhost', ...
	def __init__(self, host='', port=7654):

		super(BroadcastThread, self).__init__()

		self._isRunning = False # XXX: A locked resource
		self._lock = threading.RLock()
		self._host = host
		self._port = port

	def isRunning(self):
		with self._lock:
			return self._isRunning

	def run(self):
		"""
		Call start() to begin the thread.
		"""
		with self._lock:
			self._isRunning = True

		print 'Starting UDP service broadcast...'

		s = socket(AF_INET, SOCK_DGRAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

		bp = BroadcastPacket()

		print 'Broadcasting as available MAC %s' % bp.getMacStr()

		bp = bp.toStruct()

		running = True

		while running:
			s.sendto(bp, (self._host, self._port))
			time.sleep(0.5)

			with self._lock:
				running = self._isRunning

		print "BroadcastThread KILLED!!!"

	def kill(self):
		print "Killing BroadcastThread"
		with self._lock:
			self._isRunning = False

"""
def broadcast_get_client():
	bt = BroadcastThread()
	bt.start()

	s = socket(AF_INET, SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	s.bind(('localhost', 7765))
	s.listen(3)

	(cs, addr) = s.accept()

	bt.kill()

	return (cs, addr)
"""

