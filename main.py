#!/usr/bin/env python

import struct
import base64
from socket import *
from uuid import getnode as get_mac

def main():
	s = socket(AF_INET, SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	proto = 1
	le_state = 1
	play_state = 1
	source = 1

	le_flags = 1
	play_flags  = 1
	source_flags = 1

	fullness = 1
	point_rate = 1
	point_count = 1

	m = get_mac()
	limit = 256*256*256*256 - 1
	parts = []

	while m:
		parts.append(m & limit)
		m >>= 32

	parts.sort(reverse=True)

	mac = struct.pack('<' + 'L'*len(parts), *parts)

	pointRate = '0000000000'

	status = struct.pack('<BBBBHHHHII', \
			proto, le_state, play_state, source, le_flags, play_flags, \
			source_flags, fullness, point_rate, point_count)

	broadcastPacket = mac + pointRate + status

	while 1:

		#msg = struct.pack("<HHHI", flags, x, y, r, g, b, i, u1, u2)

		#s.sendto('Hello Everyone', ('255.255.255.255', 7654))
		#s.sendto(broadcastPacket, ('', 7654))
		s.sendto(broadcastPacket, ('localhost', 7654))

	"""

	def __init__(self, st):
		self.mac = st[:6]
		self.hw_rev, self.sw_rev, self.buffer_capacity, \
		self.max_point_rate = struct.unpack("<HHHI", st[6:16])
		self.status = Status(st[16:36])

	def dump(self, prefix = " - "):
		lines = [
			"MAC: " + ":".join(
				"%02x" % (ord(o), ) for o in self.mac),
			"HW %d, SW %d" %
				(self.hw_rev, self.sw_rev),
			"Capabilities: max %d points, %d kpps" %
				(self.buffer_capacity, self.max_point_rate)
		]
		for l in lines:
			print prefix + l
		self.status.dump(prefix)
	"""


def listen():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server.bind(('', 80))

	server.listen(3)

	while 1:
		#accept connections from outside
		(clientsocket, address) = serversocket.accept()
		#now do something with the clientsocket
		#in this case, we'll pretend this is a threaded server
		ct = client_thread(clientsocket)
		ct.run()

if __name__ == '__main__':
	main()

