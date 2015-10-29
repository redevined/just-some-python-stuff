#!/usr/bin/env python


class Timer(object) :
	
	def __init__(self, func = None, output = print) :
		self.func = func
		self.output = output
	
	def __call__(self, *args, **kwargs) :
		if self.func :
			self.__enter__()
			res = self.func(*args, **kwargs)
			self.__exit__()
			return res
		else :
			raise TypeError("'Timer' object is not used as a decorator and therefore not callable")
	
	def __enter__(self, *args) :
		self.t0 = time.time()
	
	def __exit__(self, *args) :
		dt = time.time() - self.t0
		self.output("=> Execution{func} took {time:.6} seconds".format(func = " of {0}()".format(self.func.__name__) if self.func else "", time = dt))