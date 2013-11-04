import struct
import socket

from errors import *

class SocketReader(object):
	def __init__(self, socket):
		self._socket = socket

		self._kbytes = 8
		self._buf = bytearray(1024 * self._kbytes)
		self._view = memoryview(self._buf)

		self._nextStart = 0 # start byte index
		self._cmdStart = 0 # start of command index

		self._cmdIndex = 0

		# If we got cut off at a kb boundary, we need to know
		# The instruction we already read.
		self._prereadLen = 0
		self._prereadStart = 0
		self._prereadType = ''

		self._prereadEnd = 0

		self._start = 0
		self._end = 0

	def _recv_socket(self):
		st = self._end

		try:
			view = self._view[st: st + 1024]
			nbytes = self._socket.recv_into(view, 1024)

			self._nextStart = ( st + 1024 ) % len(self._buf)
			ed = st + nbytes

		except socket.timeout as e:
			raise SocketTimeout()

		if not nbytes:
			raise SocketBroken('Socket Connection Broken')

		return st, ed

	def _get_cmd(self, index):
		view = self._view[index:index+3]
		cmd = view[0]
		length = 1024
		if cmd == 'd':
			c, length = struct.unpack('<cH', str(view.tobytes()))
		return (cmd, length)

	def read(self):
		st, ed = self._recv_socket()

		cmd, length = self._get_cmd(self._cmdIndex)

		scanned = 0
		if start != self._cmdIndex:
			before = start - self._cmdIndex
			scanned = before + 1024

			if scanned >= length:
				self._cmdIndex = self._start
				return # CASE IS DONE

		cmdSt = self.cmdIndex
		cmdEd = self.cmdIndex + length

		self.cmdIndex = self.cmdEd

		if length != 1024:
			pass

		start = self._start
		kbs = 1
		if self._prereadLen and self._prereadType != 'd':
			start = self._prereadStart
			kbs += 1

		return self._get_packet()

