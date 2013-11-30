#!/usr/bin/env python


from oldlib import dac
from find_dac import *
from net.macs import *

# TODO IMPORT SIMPLIFICATION
from vdac.vdac import VirtualDac
from repeater.repeater import RepeaterProcess

DEVICE_MAC = MAC_ETHERDREAM_A

def main():

	p1 = VirtualDac(
			host='255.255.255.255'
	)
	q = p1.get_queue()
	p1.start()

	p2 = RepeaterProcess(DEVICE_MAC)
	p2.start()

	p1.join()
	p2.join()

if __name__ == '__main__':
	main()

