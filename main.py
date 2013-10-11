#!/usr/bin/env python

import struct
import time
import base64
from socket import *
from uuid import getnode as get_mac
from multiprocessing import Process, Queue

from broadcast import BroadcastPacket

def broadcast_thread():
	s = socket(AF_INET, SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	bp = BroadcastPacket()
	broadcastPacket = bp.getStruct()

	while 1:
		#s.sendto(broadcastPacket, ('255.255.255.255', 7654))
		#s.sendto(broadcastPacket, ('', 7654))
		s.sendto(broadcastPacket, ('localhost', 7654))


# TODO TODO TODO
def etherdream_thread():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(('', 7765))
	server.listen(3)

	while 1:
		#accept connections from outside
		(clientsocket, address) = serversocket.accept()
		#now do something with the clientsocket
		#in this case, we'll pretend this is a threaded server
		ct = client_thread(clientsocket)
		ct.run()

def main():
	p1 = Process(target=broadcast_thread, args=())
	p1.start()

	p2 = Process(target=etherdream_thread, args=())
	p2.start()

	while True:
		time.sleep(100000)

if __name__ == '__main__':
	main()

