#!/usr/bin/env python

import struct
import thread
import threading
import time

from socket import *
from multiprocessing import Process, Queue

from errors import *
from broadcast import BroadcastPacket as BroadcastPacket2
from broadcast import BroadcastThread

from streamer import *

from oldlib import dac
from find_dac import *
from macs import *

DEVICE_MAC = MAC_ETHERDREAM_A

from process.courier import *

from vdac.vdac import VirtualDac # TODO IMPORT SIMPLIFICATION

def main():

	#p3 = RepeaterProcess(DEVICE_MAC)
	#queue = p3.getQueue()
	#p3.start()

	#p2 = Process(target=etherdream_process, args=(queue,))
	#p2.start()

	p2 = VirtualDac()
	q = p2.get_queue()
	p2.start()

	while True:
		time.sleep(100000)

if __name__ == '__main__':
	main()

