import sys

import struct
import threading
import thread
import select

from socket import *

from uuid import getnode as get_mac # TODO: Not really necessary

from broadcast import *
from errors import *

from packet import *
from errors import *
from reader import *

MAC_ADDRESS = get_mac()


class EtherdreamThread(threading.Thread):
	def __init__(self, sock, address, queue):
		#print 'test'
		threading.Thread.__init__(self)
		self._socket = sock
		self.address = address
		self._queue = queue
		self._reader = SocketReader(sock)

		sock.settimeout(0.1) # XXX XXX XXX NOT SURE IF BAD PRACTICE :(

	def communicate(self):
		self.send_hello()
		self.main()

	def send_hello(self):
		#print 'sending hello'
		hello = ResponsePacket('?')
		respPacket = hello.getStruct()
		self._socket.send(respPacket)

	def send_prepared(self):
		#print 'sending prepare'
		hello = ResponsePacket('p')
		respPacket = hello.getStruct()
		self._socket.send(respPacket)

	def respond_begin(self):
		#print 'sending begin'
		p = ResponsePacket('b')
		respPacket = p.getStruct()
		self._socket.send(respPacket)
		#print 'sent begin'

	def respond_data(self):
		p = ResponsePacket('d')
		respPacket = p.getStruct()
		self._socket.send(respPacket)

	def handle_packet(self, packet):
		buf = packet.getBuffer()
		#print 'handle_packet:', len(buf)

		#print 'Buffer Len: %d' % len(buf)
		t = packet.getType()

		if t == PacketTypes.DATA:
			if self._queue:
				self._queue.put_nowait(buf)
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
			try:
				buf = self._reader.read()
				packet = ReceivedCommandPacket(buf)
				self.handle_packet(packet)
			except:
				print 'Exception!!!!'
				break

	def read_command(self):
		#print "receive"
		#msg = self.socket.recv(1024)
		msg = ''
		while len(msg) < 1024:
			#print 'a'
			chunk = self._socket.recv(1024 - len(msg))
			#print 'b'
			#print 'Recv: ' + chunk
			if chunk == '':
				raise SocketBroken("socket connection broken")
			msg = msg + chunk
		#print msg

def etherdream_process(queue):

	def etherdream_thread(queue):
		bcastThread = None
		s = None

		while 1:
			try:
				bcastThread = BroadcastThread()
				bcastThread.start()

				s = socket.socket(AF_INET, SOCK_STREAM)
				s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
				#s.setblocking(0)
				s.bind(('localhost', 7765))
				s.listen(3)

				(clientsocket, address) = s.accept()
				#clientsocket.settimeout(0.5)
				print 'accepted! : %s' % str(address)

				bcastThread.kill()

				cs = EtherdreamThread(clientsocket, address, queue)
				cs.communicate() # XXX: Main loop

			except socket.timeout as e:
				print "Timeout exception"

			except SocketTimeout as e:
				print "Exception 2"

			except SocketException as e:
				print "Exception 3"

			except Exception as e:
				print 'Exception 4'

	while True:
		t = None
		try:
			if t:
				t.kill()
			t = thread.start_new_thread(etherdream_thread, (queue,))
			time.sleep(100000)

		except Exception as e:
			print "Exception Listener Main"
			pass

