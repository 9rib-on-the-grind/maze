import numpy as np
import copy
import maze
from enums import direction
from coords import *

class path:
	data = np.array
	start = coords
	end = coords
	prev = coords

	def __init__(self, start: coords):
		self.data = np.empty([0])
		self.start = self.prev = self.end = start

	def __add__(self, dirr: direction):
		res = copy.copy(self)
		res.append(dirr)
		return res

	def __str__(self):
		res = ''
		if len(self.data) != 0:
			for i in self.data[:-1]:
				res += str(i.name + '-')
			res += str(self.data[-1].name)
		return res

	def toCoords(self) -> list:
		res = [self.start]
		pos = self.start
		for i in self.data:
			pos = pos.move(i)
			res.append(pos)
		return res

	def append(self, dirr: direction):
		self.data = np.append(self.data, dirr)
		self.prev = self.end
		self.end = self.end.move(dirr)

	def move(self, maze: maze):
		while True: 
			directions = [i for i in maze.validDirections(self.end) if self.end.move(i) != self.prev]
			if self.end == maze.finish:
				return 'solved'
			elif len(directions) == 1:
				self.append(directions[0])
			elif maze.isDeadEnd(self.end):
				return 'dead end'
			elif maze.isFork(self.end):
				return 'fork'