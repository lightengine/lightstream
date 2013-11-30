from socket import *

from net.macs import *
from oldlib.dac import BroadcastPacket

BCAST_PORT = 7654

def find_dac_with_mac(mac):
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('0.0.0.0', BCAST_PORT))

	print 'Looking for DAC (%s)' % mac.macStr
	macsFound = set()

	while True:
		data, addr = s.recvfrom(1024)
		bp = BroadcastPacket(data)

		sz = len(macsFound)
		m = mac_to_str(bp.mac)
		macsFound.add(m)
		if sz != len(macsFound):
			print "Found EtherDream: %s" % m

		if bp.mac == mac.etherdreamStr:
			return addr[0]

