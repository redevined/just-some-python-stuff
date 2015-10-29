#!/usr/bin/env python


"""
BetterDict
----------
"""
class BetterDict(dict) :
	
	def __init__(self, obj = {}) :
		if isinstance(obj, dict) :
			obj = obj.items()
		object.__setattr__(self, "_keys", [key for key, val in obj])
		super(self.__class__, self).__init__(obj)
	
	def __repr__(self) :
		return "{0}( {1} )".format(self.__class__.__name__, str(self))
	
	def __str__(self) :
		return "{" + ", ".join("{0}: {1}".format(repr(key), repr(val)) for key, val in self) + "}"
	
	def __getattribute__(self, key) :
		if key in object.__getattribute__(self, "_keys") :
			return self[key]
		else :
			return object.__getattribute__(self, key)
	
	def __setattr__(self, key, val) :
		if key in self._keys :
			self[key] = val
		else :
			object.__setattr__(self, key, val)
	
	def __delattr__(self, key) :
		if key in self._keys :
			del(self[key])
		else :
			object.__delattr__(self, key)
	
	def __setitem__(self, key, val) :
		if key not in self._keys :
			self._keys.append(key)
		super(self.__class__, self).__setitem__(key, val)
	
	def __delitem__(self, key) :
		if key in self._keys :
			self._keys.remove(key)
		super(self.__class__, self).__delitem__(key)
	
	def __iter__(self) :
		for key in self._keys :
			yield key, self[key]
	
	def items(self) :
		return list(self)
	
	def keys(self) :
		return self._keys
	
	def values(self) :
		return [self[key] for key in self._keys]
	
	def iteritems(self) :
		for key in self._keys :
			yield key, self[key]
	
	def iterkeys(self) :
		for key in self._keys :
			yield key
	
	def itervalues(self) :
		for key in self._keys :
			yield self[key]
	
	def copy(self) :
		return self.__class__(self)
	
	def clear(self) :
		for key in self._keys :
			del(self[key])
	
	def pop(self, key, d = None) :
		if key in self._keys :
			val = self[key]
			del(self[key])
			return val
		elif d is not None :
			return d
		else :
			raise KeyError(key)
	
	def popitem(self) :
		key = self._keys[-1]
		val = self[key]
		del(self[key])
		return key, val
	
	def flip(self) :
		d = self.flipped()
		self._keys = self.values()
		for key, val in d :
			self[key] = val
	
	def flipped(self) :
		return self.__class__(zip(self.values(), self.keys()))
	
	def reverse(self) :
		self._keys.reverse()
	
	def reversed(self) :
		d = self.copy()
		d.reverse()
		return d


class Struct(dict) :

	def __init__(self, obj, *args, *kwargs) :
		for key, val in obj.items() :
			if isinstance(val, dict) :
				obj[key] = Struct(val)
		super(Struct, self).__init__(obj, *args, **kwargs)

	def __getattribute__(self, attr) :
		if attr[0] == "_" :
			return object.__getattribute__(self, attr[1:])
		else :
			return self[attr]

	def __setattr__(self, attr, val) :
		if attr[0] == "_" :
			object.__setattr__(self, attr[1:], val)
		else :
			self[attr] = val

	def __iter__(self) :
		for key, val in self._items() :
			yield (key, val)
