import numpy as np
import time
from collections import deque
from termcolor import colored
from random import shuffle
from enums import *
from coords import *
from path import *

class maze:
	data = np.array
	size = coords
	start = coords
	finish = coords
	solution = path

	def __init__(self, x: int = 33, y: int = 19):
		if not x & 1: x += 1
		if not y & 1: y += 1
		self.data = np.full((y, x), cell.wall)
		self.size = coords(x, y)
		self.start = coords(1, 0)
		self.finish = coords(x - 2, y - 1)
		self.solution = None

	def isPassage(self, pos: coords) -> bool:
		return self.data[pos.y][pos.x] is cell.passage

	def isWall(self, pos: coords) -> bool:
		return not self.isPassage(pos)

	def isValidCoords(self, pos: coords) -> bool:
		return pos.x >= 0 and pos.x < self.size.x and pos.y >= 0 and pos.y < self.size.y

	def isFork(self, pos: coords) -> bool:
		return len(self.validDirections(pos)) > 2

	def isDeadEnd(self, pos: coords) -> bool:
		return len(self.validDirections(pos)) == 1

	def setPassage(self, pos: coords):
		self.data[pos.y][pos.x] = cell.passage

	def ungeneratedCell(self, pos: coords) -> bool:
		return self.isValidCoords(pos) and self.isWall(pos)

	def validDirections(self, pos: coords) -> list:
		return [i for i in direction if self.isValidCoords(pos.move(i)) and self.isPassage(pos.move(i))]

	def show(self, path: path = None):
		pathCoords = [] if path == None else path.toCoords()
		path = np.full((self.size.y, self.size.x), False)
		for (j, i) in pathCoords:
			path[i][j] = True
		for i in range(0, self.size.y):
			for j in range(0, self.size.x):
				left = coords(j - 1, i)
				down = coords(j, i + 1)
				if path[i][j]:
					print(colored('▀', 'blue'), end = '') if self.isValidCoords(left) and path[i][j - 1] else print(' ', end = '')
					print(colored('█', 'blue'), end = '') if self.isValidCoords(down) and path[i + 1][j] else print(colored('▀', 'blue'), end = '')
				elif self.isWall(coords(j, i)):
					print('▀', end = '') if self.isValidCoords(left) and self.isWall(left) else print(' ', end = '')
					print('█', end = '') if self.isValidCoords(down) and self.isWall(down) else print('▀', end = '')
				else:
					print('  ', end = '')
			print()

	def generate(self, delay: float = None):
		self.setPassage(self.start)
		self.recursiveBacktracker(coords(1, 1), delay)
		self.setPassage(self.finish)

	def recursiveBacktracker(self, pos: coords, delay):
		self.setPassage(pos)
		ungenerated = [i for i in direction if self.ungeneratedCell(pos.moveTwise(i))]
		shuffle(ungenerated)
		while(ungenerated != []):
			if delay is not None:
				print('\n'*10)
				self.show()
				time.sleep(delay)
			dirr = ungenerated.pop()
			self.setPassage(pos.move(dirr))
			self.recursiveBacktracker(pos.moveTwise(dirr), delay)
			ungenerated = [i for i in ungenerated if self.isWall(pos.moveTwise(i))]

	def solve(self, delay: float = None):
		paths = deque([path(self.start)])
		while paths:
			cur = paths.popleft()
			case = cur.move(self)
			if delay is not None:			
				print('\n'*10)
				self.show(cur)
				time.sleep(delay)
			if case == 'solved':
				self.solution = cur
				break
			elif case == 'fork':
				unchecked = [i for i in self.validDirections(cur.end) if cur.end.move(i) != cur.prev]
				paths.extend([cur + i for i in unchecked])