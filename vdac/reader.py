import sys
import struct
import socket
import select

class SocketReader(object):
	def __init__(self, socket):
		self._socket = socket

		self.count = 0
		self._buf = ''

	def _doRead(self):
		buf = ''
		try:
			select.select([self._socket], [], [], 0.5)
			buf = self._socket.recv(1024)

		except socket.timeout as e:
			print 'EXCEPT 1'
			raise e

		except Exception as e:
			print 'EXCEPT 2'
			raise e

		if not buf:
			print 'NOTHING READ!'
			raise Exception

		if len(self._buf):
			self._buf += buf
		else:
			self._buf = buf

	def read(self):
		self.count += 1

		buf = ''
		lengthRead = len(self._buf)
		lengthExpect = 1024

		while lengthRead < lengthExpect:
			self._doRead()

			lengthRead = len(self._buf)

			#if lengthRead == 1:
			#	lengthExpect = 1

			cmd = ''
			dataSize = 0
			if len(self._buf) > 0:
				unpack =  struct.unpack('<c', str(self._buf[0:1]))
				cmd = unpack[0]

			if cmd != 'd':
				lengthExpect = 1

			if cmd == 'd' and len(self._buf) > 2:
				c, length = struct.unpack('<cH', str(self._buf[0:3]))
				dataSize = int(length) * 18 + 3

				lengthExpect = dataSize

		buf = self._buf
		self._buf = ''

		return buf

