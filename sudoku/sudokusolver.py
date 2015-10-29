#!/usr/bin/env python

import os, sys
from copy import deepcopy
from various import generateChunks, debug, Timer


class SudokuField(object) :
	
	def __init__(self, inst, val) :
		self.sudoku = inst
		self.value = val
		self.values = set()

	def __str__(self) :
		if self == 0 :
			return "|".join(map(str, self.values))
		else :
			return str(self.value)

	def __eq__(self, val) :
		return self.value == val

	def __hash__(self) :
		return hash(self.value)

	def __nonzero__(self) :
		return bool(self.value)

	def __bool__(self) :
		return bool(self.value)

	def blankOnly(meth) :
		def wrapper(self, *args) :
			if self == 0 :
				return meth(self, *args)
		wrapper.__name__ = meth.__name__
		return wrapper

	@blankOnly
	def update(self) :
		digits = set(range(1, 10))
		row, column, square = map(set, self.sudoku.getDependencies(self))
		self.values = (digits - row) & (digits - column) & (digits - square)
		if len(self.values) == 1 :
			self.value = self.values.pop()

	@blankOnly
	def setValue(self, val) :
		self.value = val


class Sudoku(object) :
	
	def __init__(self, lines) :
		self.matrix = [ [ SudokuField(self, int(char)) for char in line ] for line in lines ]

	def __iter__(self) :
		for row in self.rows() :
			for val in row :
				yield val
	
	def __str__(self) :
		return "{0}\n{1}\n{2}\n{hr}\n{3}\n{4}\n{5}\n{hr}\n{6}\n{7}\n{8}".format(
			*[ " {0:^{s}} {1:^{s}} {2:^{s}} | {3:^{s}} {4:^{s}} {5:^{s}} | {6:^{s}} {7:^{s}} {8:^{s}} ".format(*row, s = 5) for row in self.rows() ],
			hr = "{0}|{0}|{0}".format("-"*19)
		)

	def solved(self) :
		return all(self)

	def backup(self) :
		self._backup = deepcopy(self.matrix)

	def restore(self) :
		self.matrix = self._backup

	def getDependencies(self, f) :
		return self.getGroupOf(self.rows(), f), self.getGroupOf(self.columns(), f), self.getGroupOf(self.squares(), f)

	def getGroupOf(self, groups, field) :
		for group in groups :
			for val in group :
				if val is field :
					return group

	def getFields(self) :
		return [ field for field in self ]

	def getBlankFields(self) :
		return [ field for field in self if not field ]

	def rows(self) :
		for row in self.matrix :
			yield [ val for val in row ]

	def columns(self) :
		for i in range(9) :
			yield [ row[i] for row in self.matrix ]

	def squares(self) :
		for y in range(9)[::3] :
			for x in range(9)[::3] :
				yield [ self.matrix[i+y][j+x] for i in range(3) for j in range(3) ]


def repeat(func) :
	def wrapper(puzzle) :
		puzzle_copy = str()
		while puzzle_copy != str(puzzle) :
			puzzle_copy = str(puzzle)
			func(puzzle)
	wrapper.__name__ = func.__name__
	return wrapper

@repeat
def calcPossibleValues(puzzle) :
	for field in puzzle :
		field.update()

@repeat
def searchIndividualValues(puzzle) :
	for groups in (puzzle.rows(), puzzle.columns(), puzzle.squares()) :
		for group in groups :
			vals = [ val for field in group for val in field.values ]
			for val in range(1, 10) :
				if vals.count(val) == 1 :
					for field in group :
						if val in field.values :
							field.setValue(val)

@repeat
def solve(puzzle) :
	calcPossibleValues(puzzle)
	searchIndividualValues(puzzle)

def bruteForce(puzzle) :
	def force(fields) :
		if fields :
			for i, field in enumerate(fields) :
				for val in field.values :
					field.setValue(val)
					if force(fields[i+1:]) :
						return True
		else :
			solve(puzzle)
			return puzzle.solved() or puzzle.restore()

	puzzle.backup()
	for r in range(len(puzzle.getFields())) :
		for i in range(len(puzzle.getFields())) :
			if force(puzzle.getFields()[i:i+r+1]) :
				return

@Timer
def main(fname) :
	with open(fname) as f :
		chars = [ char for char in f.read().replace(".", "0") if char.isdigit() ]
		if len(chars) != 9 * 9 :
			print "Bad Sudoku format."
			return
		puzzle = Sudoku(generateChunks(chars, 9))

	print puzzle
	print "\nSolving Sudoku...\n"
	solve(puzzle)

	if not puzzle.solved() :
		bruteForce(puzzle)
		if not puzzle.solved() :
			print "Sudoku is not solvable."
	print puzzle


if __name__ == "__main__" :
	main(sys.argv[1])
