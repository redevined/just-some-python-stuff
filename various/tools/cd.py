#!/usr/bin/env python


class CD() :
	
	def __init__(self, path) :
		self.path = path
	
	def __enter__(self, *args) :
		self._switch(self.path)
	
	def __exit__(self, *args) :
		self._switch(self.path)
	
	def _switch(self, path) :
		self.path = os.getcwd()
		os.chdir(path)