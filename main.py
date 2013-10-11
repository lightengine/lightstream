#!/usr/bin/env python

import struct
import base64
from socket import *
from uuid import getnode as get_mac

"""
My EtherDeam's Output
=====================
- MAC: 00:04:a3:87:28:cd
- HW 2, SW 2
- Capabilities: max 1799 points, 100000 kpps
- Light engine: state 0, flags 0x0
- Playback: state 0, flags 0x0
- Buffer: 0 points
- Playback: 0 kpps, 0 points played
- Source: 0, flags 0x0
"""

def packed_mac(mac=None):
	if not mac:
		mac = get_mac()

	byts = []
	while mac > 0:
		d = mac & 0xFF
		byts.append('%02x' %d)
		mac >>= 8

	byteStr = int(''.join(byts), 16)

	return struct.pack('<' + 'Q', byteStr)[0:6] # Two wasted bits

def packed_info():
	hw_rev = int('%02x' % 2, 16)
	sw_rev = int('%02x' % 2, 16)
	buffer_cap = int('%02x' % 1799, 16)
	max_pt_rate= int('%04x' % 100000, 16)

	return struct.pack('<HHHI', hw_rev, sw_rev, buffer_cap, max_pt_rate)[0:10]

def packed_status():
	proto = 0
	le_state = 0
	play_state = 0
	source = 0

	le_flags = 0
	play_flags  = 0
	source_flags = 0

	fullness = 0
	point_rate = 0
	point_count = 0

	return struct.pack('<BBBBHHHHII', \
			proto, le_state, play_state, source, le_flags, play_flags, \
			source_flags, fullness, point_rate, point_count)

def main():
	s = socket(AF_INET, SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	mac = packed_mac()
	info = packed_info()
	status = packed_status()

	broadcastPacket = mac + info + status

	while 1:
		#s.sendto(broadcastPacket, ('255.255.255.255', 7654))
		#s.sendto(broadcastPacket, ('', 7654))
		s.sendto(broadcastPacket, ('localhost', 7654))

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

