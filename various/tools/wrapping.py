#!/usr/bin/env python


"""
Wrapper
-------

Wraps around an object and acts like the wrapped object.

Constructor:
	>>> Wrapper(obj = None)
	
	The passed object can be of any type and can later be changed through the '_' attribute.
	Any operation performed on the wrapper will be performed on the object.

Example usage:
	>>> class Test() :
	... 	def __init__(self, smth) : self.smth = smth
	... 	def print(self) : print self.smth.test
	...
	>>> class Smth() :
	... 	def __init__(self, test) : self.test = test
	...
	>>> test = Test(Smth(test))
	NameError: name 'test' is not defined
	>>> w = Wrapper()
	>>> test = Test(w)
	>>> w._ = Smth(test)
	>>> test.print()
	<__main__.Test object>
"""
class Wrapper(object) :
	
	def __init__(self, obj = None) :
		self.obj = obj
	
	def __repr__(self) :
		obj = object.__getattribute__(self, "obj")
		return repr(obj)
	
	def __str__(self) :	
		obj = object.__getattribute__(self, "obj")
		return str(obj)
	
	def __call__(self, *args, **kwargs) :
		obj = object.__getattribute__(self, "obj")
		return obj(*args, **kwargs)
	
	def __getattribute__(self, attr) :
		obj = object.__getattribute__(self, "obj")
		if attr == "_" :
			return obj
		else :
			return getattr(obj, attr)
	
	def __setattr__(self, attr, val) :
		obj = object.__getattribute__(self, "obj")
		if attr == "_" :
			object.__setattr__(self, "obj", val)
		else :
			setattr(obj, attr, val)
	
	def __delattr__(self, attr) :
		obj = object.__getattribute__(self, "obj")
		delattr(obj, attr)
	
	def __getitem__(self, index) :
		obj = object.__getattribute__(self, "obj")
		return obj[index]
	
	def __setitem__(self, index, val) :
		obj = object.__getattribute__(self, "obj")
		obj[index] = val
	
	def __delitem__(self, index, val) :
		obj = object.__getattribute__(self, "obj")
		del(obj[index])


"""
SafeNav
-------

Wrapper that emulates the SafeNavigation-Operator like in Groovy.
If a non-existent attribute or item is accessed, the SafeNav object returns an alternative object instead of throwing an exception.

Constructor:
	>>> SafeNav(obj, alt = alt)
	
	The first argument 'obj' is the wrapped object and can be of any type.
	The second parameter can either be a class or an instance.
	If 'alt' is a class, accessing a non-existent attribute or item will return a new instance of that class, otherwise it will return a reference to the provided instance.
	
	To correctly emulate the SafeNavigation-Operator known from other languages, 'alt' should be set to 'None'.
	By default, alt is set to the 'Fake' class. This offers the possibility of not having to apply a new SafeNav to every attribute access.
	E.g.:
	>>> # Object?.Method()?.Object?.Method() equals
	>>> SafeNav(SafeNav(SafeNav(Object, alt=None).Method(), alt=None).Object, alt=None).Method()
	>>> SafeNav(Object, alt=Fake).Method().Object.Method()

Example usage:
	>>> class I(int) :
	... 	def divBy(self, i) :
	... 		if i != 0 :
	... 			return I(self / i)
	...
	>>> num = I(9)
	>>> num.divBy(0).divBy(3)
	AttributeError: 'NoneType' object has no attribute 'divBy'
	>>> SafeNav(num.divBy(0)).divBy(3)
	0
	
	>>> SafeNav(num.divBy(0), alt=I(9)).divBy(3)
	3
	
	>>> str(num.divBy(0))
	'None'
	>>> str(SafeNav(num.divBy(0), alt=int))
	'0'
"""
class SafeNav(Wrapper) :
	
	def __init__(self, obj, alt = Fake) :
		self.obj = obj
		self.alt = lambda : alt() if isinstance(alt, type) else alt
	
	def __repr__(self) :
		return "SafeNavigationWrapper({})".format(repr(self))
	
	def __call__(self, *args, **kwargs) :
		obj = object.__getattribute__(self, "obj")
		Alternative = object.__getattribute__(self, "alt")
		if hasattr(obj, "__call__") :
			return obj(*args, **kwargs)
		else :
			return Alternative()
	
	def __getattribute__(self, attr) :
		obj = object.__getattribute__(self, "obj")
		Alternative = object.__getattribute__(self, "alt")
		if hasattr(obj, attr) :
			return getattr(obj, attr)
		else :
			return Alternative()
	
	def __setattr__(self, attr, val) :
		obj = object.__getattribute__(self, "obj")
		if hasattr(obj, attr) :
			setattr(obj, attr, val)
	
	def __delattr__(self, attr) :
		obj = object.__getattribute__(self, "obj")
		if hasattr(obj, attr) :
			delattr(obj, attr)
	
	def __getitem__(self, index) :
		obj = object.__getattribute__(self, "obj")
		Alternative = object.__getattribute__(self, "alt")
		if hasattr(obj, "__getitem__") :
			try :
				return obj[index]
			except IndexError :
				pass
		return Alternative()
	
	def __setitem__(self, index, val) :
		obj = object.__getattribute__(self, "obj")
		if hasattr(obj, "__setitem__") :
			try :
				obj[index] = val
			except IndexError :
				pass
	
	def __delitem__(self, index, val) :
		obj = object.__getattribute__(self, "obj")
		if hasattr(obj, "__delitem__") :
			try :
				del(obj[index])
			except IndexError :
				pass