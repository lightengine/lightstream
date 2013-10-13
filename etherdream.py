"""
Implement the Etherdream Protocol
TODO: Investigate using Twisted for this.
"""
import sys

from uuid import getnode as get_mac
import struct
import threading

MAC_ADDRESS = get_mac()

class SocketBroken(Exception):
	pass

class Packet(object):
	def __init__(self):
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
		self.mac = MAC_ADDRESS

	def getStruct(self):
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

class StatusPacket(Packet):
	pass

class ResponsePacket(Packet):
	def __init__(self, cmd='?'):
		super(ResponsePacket, self).__init__()
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

		return struct_data + struct_mac + struct_info + struct_status

class EtherdreamThread(threading.Thread):
	def __init__(self, socket, address):
		threading.Thread.__init__(self)
		self.socket = socket
		self.address = address

	def communicate(self):
		self.send_hello()

	def send_hello(self):
		"""Read a response from the DAC."""
		#data = self.read(22)
		#response = data[0]
		#cmdR = data[1]
		#status = Status(data[2:])

		hello = ResponsePacket('?')
		hello.data = '?'
		hello.cmdR = 'A'

		respPacket = hello.getStruct()
		self.socket.send(respPacket)

	def receive(self):
		print "receive"
		#msg = self.socket.recv(1024)
		msg = ''
		while len(msg) < 1024:
			print 'a'
			chunk = self.socket.recv(1024 - len(msg))
			print 'b'
			if chunk == '':
				raise SocketBroken("socket connection broken")
			msg = msg + chunk
		print msg


