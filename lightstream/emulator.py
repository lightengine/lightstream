#!/usr/bin/env python

from viz.game import *
from vdac.vdac import VirtualDac

def main():
	pt = PygameThread()
	pt.start()

	v = VirtualDac(
		host='255.255.255.255',
		queue=pt.get_queue()
	)
	v.start()

	while True:
		time.sleep(10)

if __name__ == '__main__':
	main()
