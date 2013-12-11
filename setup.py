#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name = 'lightstream',
	version = '1.0.0',
	author = 'Brandon Thomas',
	author_email = 'bt@brand.io',
	url = 'http://lasers.io',
	packages = find_packages(),
	license = 'BSD or something',
	long_description = open('README.md').read(),
	requires = [], #['pygame(>=1.9.0)'],
)

