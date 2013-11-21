
def mac_to_str(mac):
	# From Jacob Potter's EtherDream dac.py
	return ':'.join('%02x' % (ord(x), ) for x in mac)

class Mac(object):
	def __init__(self, macStr):
		self.macStr = macStr
		self.etherdreamStr = ''

		c = ''
		for p in macStr.split(':'):
			c += chr(int(p, base=16))

		self.etherdreamStr = c

# My laser projectors.
MAC_ETHERDREAM_1 = Mac('00:04:a3:3d:0b:60')
MAC_ETHERDREAM_A = Mac('00:04:a3:3d:70:9b')
MAC_ETHERDREAM_B = Mac('00:04:a3:87:28:cd')

# Computers.
MAC_COMPUTER_X120E = Mac('E8:9A:8F:19:1F:38')
MAC_COMPUTER_DARWIN = Mac('00:0E:3B:26:07:6D')

