import struct
import socket

from errors import *

class SocketReader(object):
	def __init__(self, socket):
		self._socket = socket
		self._start = 0

		self._buf = bytearray(1024*8)
		self._kb = 0

	def read(self, size=1024):
		buf = bytearray(1024*4)
		view = memoryview(buf)
		nbytes = 0

		try:
			nbytes = self._socket.recv_into(
						view[self._start : self._start + size],
						size)

		except socket.timeout as e:
			raise SocketTimeout()

		if not nbytes:
			raise SocketBroken('Socket Connection Broken')

		if not chr(buf[0]):
			raise SocketBroken('asdfasfasdf')

		tbytes = nbytes

		if chr(buf[0]) == 'd':
			print 'data packet'
			cmd, length = struct.unpack('<cH', str(buf[0:3]))

			remaining = length - nbytes
			start = nbytes

			while remaining > 0:
				print 'r'
				print 'remaining: %d' % remaining
				read = self._continue_read(buf, view, start, remaining)
				start += read
				tbytes += read
				remaining -= read

			print 'done reading data'

		return buf[0:tbytes]

	def _continue_read(self, buf, view, start=0, size=1024):
		try:
			nbytes = self._socket.recv_into(
						view[start:start+size],
						size)

		except socket.timeout as e:
			raise SocketTimeout()

		if not nbytes:
			raise SocketBroken('Socket Connection Broken')

		return nbytes

