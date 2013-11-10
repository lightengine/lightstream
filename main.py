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

from streamer import *

from oldlib import dac
from circle import CircleStream
from find_dac import *
from macs import *

DEVICE_MAC = MAC_ETHERDREAM_B

from process.listener import *
from process.courier import *

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

