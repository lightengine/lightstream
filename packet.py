import sys

import struct
import threading
import socket

from uuid import getnode as get_mac # TODO: Not really necessary

from errors import *

class PacketTypes(object):
	HELLO = 1
	PREPARE = 2
	BEGIN = 3
	DATA = 4


class Packet(object):
	def __init__(self):
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

class SendPacket(ResponsePacket):
	pass

# ==================================================================

class DacPacket(Packet):
	pass

class ReceivedPacket(Packet):
	def __init__(self, buf=''):
		self._buf = buf
		self._readCount = 0
		self._done = False

		self._isData = False
		self._dataLength = 0
		self._dataRemaining = 0

		if buf:
			self._readCount = 1
			self._done = True

	def getBuffer(self):
		return self._buf

	def reading(self):
		return not self._done

	def read(self, sock, size=1024):
		if self._done:
			return

		if self._dataRemaining:
			size = self._dataRemaining

		read = ''
		doneReading = True
		try:
			read = sock.recv(size)

		except socket.timeout as e:
			raise SocketTimeout()

		if read == '':
			raise SocketBroken('Socket Connection Broken')

		# Data commands span multiple packets.
		# TODO: Always read constant buffer size from socket.
		# Use an external provider to do so.
		if self._readCount == 0 and read[0] == 'd':
			cmd, length = struct.unpack('<cH', read[0:3])

			self._isData = True
			self._dataLength = length
			self._dataRemaining = length

		if self._dataRemaining:
			self._dataRemaining -= len(read)

		self._readCount += 1
		self._buf += read

		if self._dataRemaining > 0:
			doneReading = False

		if doneReading:
			self._done = True


class ReceivedCommandPacket(ReceivedPacket):

	def getType(self):
		if self.reading():
			return False

		if len(self._buf) < 1:
			#raise BadPacket()
			return False

		t = self._buf[0]
		if type(self._buf) == bytearray:
			t = chr(t)

		if t == 'd':
			#print 'd-type'
			return PacketTypes.DATA
		if t == '?':
			#print '?-type'
			return PacketTypes.HELLO
		if t == 'p':
			#print 'p-type'
			return PacketTypes.PREPARE
		if t == 'b':
			#print 'b-type'
			return PacketTypes.BEGIN

class ReceivedDataPacket(ReceivedCommandPacket):
	def getType(self):
		return PacketTypes.DATA


