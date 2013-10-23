#!/usr/bin/env python

import struct
import threading
import time
import base64
from socket import *
from uuid import getnode as get_mac
from multiprocessing import Process, Queue


from errors import *
from broadcast import BroadcastPacket
from etherdream import EtherdreamThread, SocketBroken

def broadcast_process():
	s = socket(AF_INET, SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	bp = BroadcastPacket()
	broadcastPacket = bp.getStruct()

	while 1:
		#s.sendto(broadcastPacket, ('255.255.255.255', 7654))
		#s.sendto(broadcastPacket, ('', 7654))
		s.sendto(broadcastPacket, ('localhost', 7654))


def etherdream_process():
	s = socket(AF_INET, SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind(('localhost', 7765))
	s.listen(3)

	while 1:
		#accept connections from outside
		(clientsocket, address) = s.accept()
		#now do something with the clientsocket
		#in this case, we'll pretend this is a threaded server
		#msg = receive(s)
		print "accepted: %s" % str(address)
		try:
			cs = EtherdreamThread(clientsocket, address)
			cs.communicate()
		except SocketException as e:
			print "Etherdream got an exception..."
			print e

		#ct = client_thread(clientsocket)
		#ct.run()

def main():
	p1 = Process(target=broadcast_process, args=())
	p1.start()

	p2 = Process(target=etherdream_process, args=())
	p2.start()

	while True:
		time.sleep(100000)

if __name__ == '__main__':
	main()

