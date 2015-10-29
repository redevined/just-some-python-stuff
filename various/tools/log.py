#!/usr/bin/env python


def debug(*args, **kwargs) :
	print("\n### DEBUG {0} ###\n".format(datetime.today().isoformat()))
	for arg in args :
		print("  {0}".format(arg))
	for key, val in kwargs.items() :
		print("  {0} = {1}".format(key, val))
	print("\n{0}\n".format("#" * 40))