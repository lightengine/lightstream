#!/usr/bin/env python

import time
import thread
import threading
from multiprocessing import Process, Queue

from oldlib import dac
from find_dac import *
from net.macs import *

DEVICE_MAC = MAC_ETHERDREAM_A

from vdac.vdac import VirtualDac # TODO IMPORT SIMPLIFICATION
from process.courier import *

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

