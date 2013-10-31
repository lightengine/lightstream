from socket import *
from oldlib.dac import BroadcastPacket

BCAST_PORT = 7654

def find_dac_with_mac(mac):
	s = socket(AF_INET, SOCK_DGRAM)
	s.bind(('0.0.0.0', BCAST_PORT))

	while True:
		data, addr = s.recvfrom(1024)
		bp = BroadcastPacket(data)

		if bp.mac == mac.etherdreamStr:
			return addr

