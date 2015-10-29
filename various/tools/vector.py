#!/usr/bin/env python


"""
Vector
------
"""
class Vector(list) :
	
	def __init__(self, *vals) :
		for val in vals :
			if not (isinstance(cal, int) or isinstance(val, float)) :
				raise TypeError("coordinates have to be numerical type")
		super(self.__class__, self).__init__(vals)
	
	def __repr__(self) :
		return "Vector{0}".format(str(self))
	
	def __str__(self) :
		return "({0})".format(" | ".join(map(str, self)))
	
	def __getattribute__(self, attr) :
		if attr in ("x", "y", "z") :
			return self[{"x" : 0, "y" : 1, "z" : 2}[attr]]
		else :
			return super(self.__class__, self).__getattribute__(attr)
	
	def __setattr__(self, attr, val) :
		if attr in ("x", "y", "z") :
			self[{"x" : 0, "y" : 1, "z" : 2}[attr]] = val
		else :
			super(self.__class__, self).__setattr__(attr, val)
	
	def __delattr__(self, attr) :
		if attr in ("x", "y", "z") :
			del(self[{"x" : 0, "y" : 1, "z" : 2}[attr]])
		else :
			super(self.__class__, self).__delattr__(attr)
	
	def __setitem__(self, index, val) :
		if not (isinstance(val, int) or isinstance(val, float)) :
			raise TypeError("coordinates have to be numerical type")
		else :
			super(self.__class__, self).__setitem__(index, val)