from multiprocessing.queues import Queue

class SmallQueue(Queue):

	def __init__(self, maxsize=5):
		super(SmallQueue, self).__init__(maxsize=maxsize)
		self._maxsize = maxsize

	def put_nowait(self, item):
		if self.qsize() >= self._maxsize:
			self.get_nowait() # discard one

		super(SmallQueue, self).put_nowait(item)

