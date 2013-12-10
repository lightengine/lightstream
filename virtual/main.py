#!/usr/bin/env python

import sys

from oldlib import dac
from find_dac import *
from net.macs import *

# TODO IMPORT SIMPLIFICATION
from vdac.vdac import VirtualDac
from repeater.repeater import RepeaterProcess

NAMED = {
	'a': MAC_ETHERDREAM_A.macStr,
	'b': MAC_ETHERDREAM_B.macStr,
	'c': MAC_ETHERDREAM_B.macStr,
}

def parse_args():
	from argparse import ArgumentParser

	parser = ArgumentParser(description='Documentation TODO.')

	parser.add_argument('--send', metavar='MAC', type=str,
					help='Mac to send to (default: ANY mac.)',
					default='')

	parser.add_argument('--sendKey', metavar='KEY', type=str,
					help='Predefined mac to send to.',
					default='')

	parser.add_argument('--broadcast', metavar='MAC', type=str,
					help='Broadcast Mac (default: hardware mac.)',
					default='')

	return parser.parse_args()

def get_args():
	args = parse_args()

	print args
	send = None
	broadcast = None

	if args.send:
		send = args.send

	elif args.sendKey:
		n = args.sendKey.lower()
		if n in NAMED:
			send = NAMED[n]

	if args.broadcast:
		broadcast = args.broadcast

	return {
		'send': send,
		'broadcast': broadcast,
	}

def main():
	args = get_args()

	print args

	p1 = VirtualDac(
		host='255.255.255.255'
	)
	p1.start()

	p2 = RepeaterProcess(send_mac=args['send'], queue=p1.get_queue())
	p2.start()

	p1.join()
	p2.join()

if __name__ == '__main__':
	main()

