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

from streamer import *

from oldlib import dac
from circle import CircleStream
from find_dac import *
from macs import *

DEVICE_MAC = MAC_ETHERDREAM_B

def etherdream_process(queue):

	def etherdream_thread(queue):
		bcastThread = BroadcastThread()
		bcastThread.start()

		s = socket(AF_INET, SOCK_STREAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.bind(('localhost', 7765))
		s.listen(3)

		while 1:
			(clientsocket, address) = s.accept()
			print 'accepted! : %s' % str(address)

			bcastThread.kill()

			try:
				print 'test1'
				cs = EtherdreamThread(clientsocket, address, queue)
				print 'test2'
				cs.communicate()
				print 'test3'

			except SocketTimeout as e:
				print e
				pass

			except SocketException as e:
				print "Etherdream got an exception..."
				print e

			bcastThread = BroadcastThread()
			bcastThread.start()

	while True:
		thread.start_new_thread(etherdream_thread, (queue,))
		time.sleep(100000)

def main():

	p3 = RepeaterProcess(DEVICE_MAC)
	queue = p3.getQueue()
	p3.start()

	p2 = Process(target=etherdream_process, args=(queue,))
	p2.start()

	while True:
		time.sleep(100000)

if __name__ == '__main__':
	main()

