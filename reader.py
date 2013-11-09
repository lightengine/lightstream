import sys
import struct
import socket

from errors import *
from circular import *

class SocketReader(object):
	def __init__(self, socket):
		self._socket = socket

		self.count = 0
		self._buf = ''

	def _doRead(self):
		print '>> _doRead'
		buf = ''
		try:
			#print 'READING 1024'
			buf = self._socket.recv(1024)
			#print 'Size: %d' % len(buf)

		except socket.timeout as e:
			raise SocketTimeout()

		if len(self._buf):
			self._buf += buf
		else:
			self._buf = buf

	def read(self):
		self.count += 1

		if self.count > 3:
			sys.exit()

		buf = ''
		lengthRead = len(self._buf)
		lengthExpect = 1024

		print "====== read ======"

		while lengthRead < lengthExpect:
			self._doRead()

			lengthRead = len(self._buf)
			#print 'Buf size: %d' % lengthRead

			#if lengthRead == 1:
			#	lengthExpect = 1

			cmd = ''
			dataSize = 0
			if len(self._buf) > 0:
				unpack =  struct.unpack('<c', str(self._buf[0:1]))
				cmd = unpack[0]

			#print 'Command was: ', cmd

			if cmd != 'd':
				lengthExpect = 1

			if cmd == 'd' and len(self._buf) > 2:
				c, length = struct.unpack('<cH', str(self._buf[0:3]))
				dataSize = int(length) * 18 + 3

				#print 'Data payload size is %d' % dataSize
				lengthExpect = dataSize

		print "Current buffer size is %d" % len(self._buf)

		#buf = self._buf[0:lengthExpect]
		#self._buf = self._buf[lengthExpect:]
		#self._buf = ''

		#self.debug()

		buf = self._buf
		self._buf = ''


		return buf

	def debug(self):

		i = 0
		s = []
		for i in range(len(self._buf)):
			if i % 2**9 == 0:
				print ','.join(s)
				print i
				s = []

			unpack =  struct.unpack('<c', str(self._buf[i:i+1]))
			cmd = unpack[0]

			if cmd == 'd':
				l2 = 0
				if i + 3 < len(self._buf):
					c2, l2 = struct.unpack('<cH', str(self._buf[i:i+3]))
					l2 = int(l2)

				print '`d` found at: %d, length: %d' % (i, l2)
				print ','.join(s)

				s = []

			s.append(cmd)

		#self._buf = ''
		#print ','.join(s)


