"""
Implement the Etherdream Protocol
TODO: Investigate using Twisted for this.
"""
import sys

import struct
import threading
import socket

from uuid import getnode as get_mac # TODO: Not really necessary

from packet import *
from errors import *

MAC_ADDRESS = get_mac()

class EtherdreamThread(threading.Thread):
	def __init__(self, socket, address):
		threading.Thread.__init__(self)
		self.socket = socket
		self.address = address

		socket.settimeout(0.1) # XXX XXX XXX NOT SURE IF BAD PRACTICE :(

	def communicate(self):
		self.send_hello()
		self.main()

		"""
		self.send_hello()
		self.read_command()
		self.send_prepared()
		"""

	def send_hello(self):
		#print 'sending hello'
		hello = ResponsePacket('?')
		respPacket = hello.getStruct()
		self.socket.send(respPacket)

	def send_prepared(self):
		#print 'sending prepare'
		hello = ResponsePacket('p')
		respPacket = hello.getStruct()
		self.socket.send(respPacket)

	def respond_begin(self):
		p = ResponsePacket('b')
		respPacket = p.getStruct()
		self.socket.send(respPacket)

	def respond_data(self):
		p = ResponsePacket('d')
		respPacket = p.getStruct()
		self.socket.send(respPacket)

	def handle_packet(self, packet):
		buf = packet.getBuffer()
		#print 'handle_packet:', len(buf)

		t = packet.getType()

		if t == PacketTypes.DATA:
			#print 'data packet'
			self.respond_data()
			return

		if t == PacketTypes.BEGIN:
			#print 'begin packet'
			self.respond_begin()
			return

		if t == PacketTypes.PREPARE:
			#print 'prepare packet'
			self.send_prepared()
			return

	def main(self):
		while 1:
			packet = ReceivedCommandPacket()

			while packet.reading():
				packet.read(self.socket, 1024)

			self.handle_packet(packet)

	def read_command(self):
		#print "receive"
		#msg = self.socket.recv(1024)
		msg = ''
		while len(msg) < 1024:
			#print 'a'
			chunk = self.socket.recv(1024 - len(msg))
			#print 'b'
			#print 'Recv: ' + chunk
			if chunk == '':
				raise SocketBroken("socket connection broken")
			msg = msg + chunk
		#print msg


