#/usr/bin/env python


"""
CharSequence
------------
"""
class CharSequence(list) :
	
	def __init__(self, seq = "") :
		super(self.__class__, self).__init__(str().join(seq))
		
	def __repr__(self) :
		return "CharSequence('{0}')".format(self)
	
	def __str__(self) :
		return str().join(self)
	
	def __setitem__(self, index, char) :
		super(self.__class__, self).__setitem__(index, str(char))
	
	def __getslice__(self, lower, upper) :
		return CharSequence(super(self.__class__, self).__getslice__(lower, upper))
	
	def __setslice__(self, lower, upper, seq) :
		super(self.__class__, self).__setslice__(lower, upper, str(seq))
	
	def __add__(self, seq) :
		return super(self.__class__, self).__add__(CharSequence(seq))
	
	def __radd__(self, seq) :
		return self.__add__(seq)
	
	def __iadd__(self, seq) :
		super(self.__class__, self).__iadd__(CharSequence(seq))
	
	def __mul__(self, i) :
		return CharSequence(super(self.__class__, self).__mul__(i))
	
	def __rmul__(self, i) :
		return self.__mul__(i)


def splitByBrackets(s) :
	pass #?


def generateChunks(seq, size) :
	for i in range(len(seq))[::size] :
		yield seq[ i : i+size ]