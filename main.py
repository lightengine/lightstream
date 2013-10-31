#!/usr/bin/env python

import struct
import thread
import threading
import time
import base64

from socket import *
from uuid import getnode as get_mac
from multiprocessing import Process, Queue

from errors import *
from broadcast import BroadcastPacket as BroadcastPacket2
from broadcast import BroadcastThread
from etherdream import EtherdreamThread, SocketBroken

from oldlib import dac
from circle import CircleStream
from find_dac import *
from macs import *

DEVICE_MAC = MAC_ETHERDREAM_B

def etherdream_process():
	"""
	def broadcast_thread():
		s = socket(AF_INET, SOCK_DGRAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

		bp = BroadcastPacket2()
		broadcastPacket = bp.getStruct()

		while 1:
			#s.sendto(broadcastPacket, ('255.255.255.255', 7654))
			s.sendto(broadcastPacket, ('', 7654))
			#s.sendto(broadcastPacket, ('localhost', 7654))
	"""


	def etherdream_thread(bcastThread):
		s = socket(AF_INET, SOCK_STREAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.bind(('localhost', 7765))
		s.listen(3)

		while 1:
			(clientsocket, address) = s.accept()
			print 'accepted: %s' % str(address)

			bcastThread.kill()

			try:
				cs = EtherdreamThread(clientsocket, address)
				cs.communicate()

			except SocketTimeout as e:
				pass

			except SocketException as e:
				print "Etherdream got an exception..."
				print e

			#ct = client_thread(clientsocket)
			#ct.run()

	bcastThread = BroadcastThread()

	while True:
		thread.start_new_thread(etherdream_thread, (bcastThread,))
		bcastThread.run()
		time.sleep(100000)

def outbound_process():
	while True:
		try:
			#addr = dac.find_first_dac()
			addr = find_dac_with_mac(DEVICE_MAC)
			print "Found %s at addr %s" % (DEVICE_MAC.macStr, addr)

			d = dac.DAC(addr)
			s = CircleStream()
			d.play_stream(s)

		except Exception as e:
			print 'Exception'
			print e
			pass

def main():

	p2 = Process(target=etherdream_process, args=())
	p2.start()

	p3 = Process(target=outbound_process, args=())
	p3.start()

	while True:
		time.sleep(100000)

if __name__ == '__main__':
	main()

