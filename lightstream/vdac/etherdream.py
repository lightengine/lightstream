import time
import socket
import struct
import threading
from Queue import Full as QueueFullException

from reader import SocketReader
from packets import ResponsePacket

class EtherdreamThread(threading.Thread):

	# Response packets to send the client
	_HELLO = ResponsePacket('?').getStruct()
	_PREPARE = ResponsePacket('p').getStruct()
	_BEGIN = ResponsePacket('b').getStruct()
	_DATA = ResponsePacket('d').getStruct()

	def __init__(self, sock, address, queue):
		threading.Thread.__init__(self)

		self._socket = sock
		self.address = address
		self._queue = queue
		self._reader = SocketReader(sock)

		# Attempt to send linger
		# http://stackoverflow.com/q/6439790
		l_onoff = 1
		l_linger = 0
		sock.setsockopt(
				socket.SOL_SOCKET,
				socket.SO_LINGER,
				struct.pack('ii', l_onoff, l_linger))

		sock.settimeout(0.1) # XXX XXX XXX NOT SURE IF BAD PRACTICE :(

	def main(self):
		self.send_hello()

		while 1:
			try:
				buf = self._reader.read()
				self.handle_packet(buf)

			except QueueFullException as e:
				print 'EtherdreamThread: Queue full'
				time.sleep(0.01)
				continue
				#raise e

			except socket.timeout as e:
				# Must restart comms with DAC.
				print 'EtherdreamThread.main() exception'
				print 'Closing socket...'
				print type(e)
				print str(e)
				self._socket.shutdown(socket.SHUT_RDWR)
				self._socket.close()
				raise e

			except Exception as e:
				print 'EtherdreamThread.main() exception'
				print type(e)
				print str(e)
				break

	def handle_packet(self, packet):
		if len(packet) < 1:
			return False

		t = packet[0]
		if type(packet) == bytearray:
			t = chr(t)

		# `data` is most frequent packet type
		if t == 'd':
			if self._queue:


				#l = self._queue.qsize()
				#w = l * 0.001
				#print 'sleep %f' % w
				#time.sleep(w)
				while 1:
					try:
						self._queue.put_nowait(packet)
						break

					except QueueFullException:
						print 'QueueFullException [handle_packet()]'
						time.sleep(0.01)
						#print 'Killing thread.'
						#self._socket.shutdown(socket.SHUT_RDWR)
						#self._socket.close()
						#raise e

			self.respond_data()
			return

		if t == '?':
			return # hello packet

		if t == 'p':
			self.send_prepare()
			return

		if t == 'b':
			self.respond_begin()
			return

	def send_hello(self):
		print 'sending hello'
		self._socket.send(self._HELLO)

	def send_prepare(self):
		print 'sending prepare'
		self._socket.send(self._PREPARE)

	def respond_begin(self):
		print 'sending begin'
		self._socket.send(self._BEGIN)

	def respond_data(self):
		self._socket.send(self._DATA)

