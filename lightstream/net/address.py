import socket
import struct

def get_local_address(remote_host='google.com'):
	"""
	Get the local network address
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((remote_host, 80))
	ip = s.getsockname()[0]
	s.close()
	return ip

def get_broadcast_address(local_address, subnet='255.255.255.255'):
	"""
	Calculate the broadcast address from the local address and subnet.
	"""
	local  = struct.unpack('>L', socket.inet_aton(local_address))[0]
	subnet = struct.unpack('>L', socket.inet_aton(subnet))[0]
	bcast  = local | (subnet ^ 0xffffffff)

	return socket.inet_ntoa(struct.pack('>L', bcast))

