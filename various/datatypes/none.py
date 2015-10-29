#!/usr/bin/env python


"""
Fake
----

Alternate 'None', designed to not throw exceptions while accessing non-existent attributes or usage in common operations.

Currently supports:
	- Calling as a function
	- Get, set and delete operations on attributes
	- Common list operations
	- Common numerical operations

Example usage:
	>>> class Hello() :
	... 	def say(self) :
	... 		print "Hello World!"
	...
	>>> say_something = False
	>>> hello = Hello() if say_something else Fake()
	>>> hello.say()
	
	>>> # Usage with 'SafeNav' object
	>>> SafeNav(hello, alt = Fake).say().upper().center(30)
"""
class Fake(object) :
	
	def __init__(self, *args, **kwargs) : pass
	
	def __repr__(self) : return "Fake"
	
	def __str__(self) : return "Fake"
	
	def __call__(self, *args, **kwargs) : return Fake()
	
	def __getattribute__(self, *args) : return Fake()
	
	def __setattr__(self, *args) : pass
	
	def __delattr__(self) : pass
	
	def __getitem__(self, *args) : return Fake()
	
	def __setitem__(self, *args) : pass
	
	def __delitem__(self) : pass
	
	def __add__(self, obj) : return obj
	
	def __radd__(self, obj) : return obj
	
	def __sub__(self, obj) : return obj
	
	def __rsub__(self, obj) : return -obj
	
	def __mul__(self, obj) : return obj
	
	def __rmul__(self, obj) : return obj
	
	def __div__(self, obj) : return obj
	
	def __rdiv__(self, obj) : return type(obj)()
	
	def __truediv__(self, obj) : return obj
	
	def __rtruediv__(self, obj) : return type(obj)()
	
	def __floordiv__(self, obj) : return obj
	
	def __rfloordiv__(self, obj) : return type(obj)()
	
	def __nonzero__(self) : return False
	
	def __bool__(self) : return False
	
	def __len__(self) : return 0
	
	def __contains__(self, *args) : return False