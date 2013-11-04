
class CircularByteBuffer(object):
	SZ = 1024

	def __init__(self, socket, length):
		if self.SZ > 1 and length % self.SZ:
			raise Exception('Cannot use size that isn\'t multiple of 1024.')

		self._length = length + self.SZ # Extra element
		self._start = 0
		self._end = 0
		self._buf = bytearray(self._length)
		self._view = memoryview(self._buf)
		self._socket = socket

	def is_full(self):
		return (self._end + self.SZ) % self._length == self._start

	def is_empty(self):
		return self._end == self._start

	def push(self, item):
		self._view[self._end : self._end +self.SZ] = item
		self._end = (self._end + self.SZ) % self._length
		if self._end == self._start:
			self._start = (self._start + self.SZ) % self._length

	def fetch(self):
		view = self._view[self._end : self._end +self.SZ]
		nbytes = self._socket.recv_into(view, self.SZ)
		self._end = (self._end + self.SZ) % self._length
		if self._end == self._start:
			self._start = (self._start + self.SZ) % self._length

	def read(self):
		view = self._view[self._start:self._start + self.SZ]
		self._start = (self._start + self.SZ) % self._length
		return view

