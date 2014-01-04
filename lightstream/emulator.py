#!/usr/bin/env python

import socket
import struct

from argparse import ArgumentParser

from net.address import *
from viz.game import *
from vdac.vdac import VirtualDac

def parse_args():
	parser = ArgumentParser(
				description=' '.join([
					'Run an EtherDream laser projector emulator.',
					'Arguments configure networking, etc.',
				]))

	ngroup = parser.add_argument_group('Networking')

	ngroup.add_argument('-s', '--subnet',
				required=False,
				metavar='IP',
				default='255.255.255.255',
				type=str,
				help='Set the subnet mask (default: 255.255.255.255)')

	ngroup.add_argument('-b', '--bcast',
				required=False,
				metavar='IP',
				default='',
				type=str,
				help=' '.join([
					'Manually set broadcast address',
					'(eg. 255.255.255.255)',
				]))

	ngroup.add_argument('-t', '--test',
				required=False,
				metavar='HOST',
				default='google.com',
				type=str,
				help='Lookup local address against.')


	return parser.parse_args()

def main():
	args = parse_args()
	print args

	broadcast = args.bcast
	subnet = args.subnet

	if not broadcast:
		local = get_local_address(args.test)
		broadcast = get_broadcast_address(local, subnet)

	print 'Broadcast address is {}'.format(broadcast)

	pt = PygameThread()
	pt.start()

	v = VirtualDac(
		host=broadcast,
		queue=pt.get_queue()
	)
	v.start()

	while True:
		time.sleep(100000000)

if __name__ == '__main__':
	main()
