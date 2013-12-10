#!/usr/bin/env python2

from socket import *

import setpath
from net.macs import *
from oldlib.dac import BroadcastPacket

BCAST_PORT = 7654

def find_dacs():
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('0.0.0.0', BCAST_PORT))

	macsFound = set()

	while True:
		data, addr = s.recvfrom(1024)
		bp = BroadcastPacket(data)

		sz = len(macsFound)
		m = mac_to_str(bp.mac)
		macsFound.add(m)
		if sz != len(macsFound):
			print "Found EtherDream: %s" % m

if __name__ == '__main__':
	find_dacs()
