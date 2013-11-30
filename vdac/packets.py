import struct
from uuid import getnode as get_mac

class BroadcastPacket(object):
	"""
	Represents an EtherDream broadcast packet.
	For example, my EtherDream outputs:
		- MAC: 00:04:a3:87:28:cd
		- HW 2, SW 2
		- Capabilities: max 1799 points, 100000 kpps
		- Light engine: state 0, flags 0x0
		- Playback: state 0, flags 0x0
		- Buffer: 0 points
		- Playback: 0 kpps, 0 points played
		- Source: 0, flags 0x0
	"""

	def __init__(self):
		self.mac = get_mac()
		self.hw_rev = 2
		self.sw_rev = 2
		self.buffer_cap = 1799
		self.max_pt_rate = 100000
		self.proto = 0
		self.le_state = 0
		self.play_state = 0
		self.source = 0
		self.le_flags = 0
		self.play_flags = 0
		self.source_flags = 0
		self.fullness = 0
		self.point_rate = 0
		self.point_count = 0

	def toStruct(self):
		byts = []
		mac = self.mac
		while mac > 0:
			d = mac & 0xFF
			byts.append('%02x' %d)
			mac >>= 8

		byteStr = int(''.join(byts), 16)

		struct_mac = struct.pack('<' + 'Q', byteStr)[:6] # Two wasted bits

		hw_rev = int('%02x' % self.hw_rev, 16)
		sw_rev = int('%02x' % self.sw_rev, 16)
		buffer_cap = int('%02x' % self.buffer_cap, 16)
		max_pt_rate= int('%04x' % self.max_pt_rate, 16)

		struct_info = struct.pack('<HHHI', hw_rev, sw_rev, \
							buffer_cap, max_pt_rate)[:10]

		proto = self.proto
		le_state = self.le_state
		play_state = self.play_state
		source = self.source

		le_flags = self.le_flags
		play_flags  = self.play_flags
		source_flags = self.source_flags

		fullness = self.fullness
		point_rate = self.point_rate
		point_count = self.point_count

		struct_status =  struct.pack('<BBBBHHHHII', \
				proto, le_state, play_state, source, le_flags, play_flags, \
				source_flags, fullness, point_rate, point_count)[:20]

		return struct_mac + struct_info + struct_status

class ResponsePacket(object):
	def __init__(self, cmd):
		self.proto = 0
		self.le_state = 0
		self.play_state = 0
		self.source = 0
		self.le_flags = 0
		self.play_flags = 0
		self.source_flags = 0
		self.fullness = 0
		self.point_rate = 0
		self.point_count = 0

		self.ack = None
		self.cmd = None
		self.setAck()
		self.setCmd(cmd)

	def setCmd(self, cmd):
		self.cmd = ord(cmd)

	def setAck(self):
		self.ack = ord('a')

	def setNack(self):
		self.ack = ord('n') # TODO: Confirm

	def getStruct(self):
		ack = int('%02x' % self.ack, 16)
		cmd = int('%02x' % self.cmd, 16)

		struct_data = struct.pack('<BB', ack, cmd)[:2]

		proto = self.proto
		le_state = self.le_state
		play_state = self.play_state
		source = self.source

		le_flags = self.le_flags
		play_flags  = self.play_flags
		source_flags = self.source_flags

		fullness = self.fullness
		point_rate = self.point_rate
		point_count = self.point_count

		struct_status =  struct.pack('<BBBBHHHHII', \
				proto, le_state, play_state, source, le_flags, play_flags, \
				source_flags, fullness, point_rate, point_count)[:20]

		return struct_data + struct_status

