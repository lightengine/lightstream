#!/usr/bin/env python

from viz.game import *

def main():
	pt = PygameThread()
	pt.start()
	while True:
		time.sleep(10)

if __name__ == '__main__':
	main()
