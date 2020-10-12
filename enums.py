from enum import Enum

class cell(Enum):
	wall = 0
	passage = 1

class direction(Enum):
	up = 1
	right = 2
	down = 3
	left = 4