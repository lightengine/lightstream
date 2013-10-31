
class SocketException(Exception):
	pass

class SocketBroken(SocketException):
	pass

class SocketTimeout(SocketException):
	pass

class BadPacket(Exception):
	pass

