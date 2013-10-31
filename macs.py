
class Mac(object):
	def __init__(self, macStr):
		self.macStr = macStr
		self.etherdreamStr = ''

		c = ''
		for p in macStr.split(':'):
			c += chr(int(p, base=16))

		self.etherdreamStr = c

# My laser projectors.
MAC_USA_= Mac('00:04:a3:3d:0b:60')
MAC_CHINA = Mac('00:04:a3:87:28:cd')

