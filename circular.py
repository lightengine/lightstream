"""
void cbInit(CircularBuffer *cb, int size) {
    cb->size  = size + 1; /* include empty elem */
    cb->start = 0;
    cb->end   = 0;
    cb->elems = (ElemType *)calloc(cb->size, sizeof(ElemType));
}

void cbFree(CircularBuffer *cb) {
    free(cb->elems); /* OK if null */ }

int cbIsFull(CircularBuffer *cb) {
    return (cb->end + 1) % cb->size == cb->start; }

int cbIsEmpty(CircularBuffer *cb) {
    return cb->end == cb->start; }

/* Write an element, overwriting oldest element if buffer is full. App can
   choose to avoid the overwrite by checking cbIsFull(). */
void cbWrite(CircularBuffer *cb, ElemType *elem) {
    cb->elems[cb->end] = *elem;
    cb->end = (cb->end + 1) % cb->size;
    if (cb->end == cb->start)
        cb->start = (cb->start + 1) % cb->size; /* full, overwrite */
}

/* Read oldest element. App must ensure !cbIsEmpty() first. */
void cbRead(CircularBuffer *cb, ElemType *elem) {
    *elem = cb->elems[cb->start];
    cb->start = (cb->start + 1) % cb->size;
}
"""

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

	def pt(self):
		print str(self._buf)
