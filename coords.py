from enums import direction

class coords:
	x = 0
	y = 0

	def __init__(self, x : int = 0, y : int = 0):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __str__(self):
		return '[' + str(self.x) + ', ' + str(self.y) + ']'

	def __iter__(self):
		yield self.x
		yield self.y

	def up(self):
		return coords(self.x, self.y - 1)

	def right(self):
		return coords(self.x + 1, self.y)

	def down(self):
		return coords(self.x, self.y + 1)

	def left(self):
		return coords(self.x - 1, self.y)

	def twiseUp(self):
		return coords(self.x, self.y - 2)

	def twiseRight(self):
		return coords(self.x + 2, self.y)

	def twiseDown(self):
		return coords(self.x, self.y + 2)

	def twiseLeft(self):
		return coords(self.x - 2, self.y)

	def move(self, dirr: direction):
		if dirr is direction.up: return self.up()
		if dirr is direction.right: return self.right()
		if dirr is direction.down: return self.down()
		if dirr is direction.left: return self.left()

	def moveTwise(self, dirr: direction):
		if dirr is direction.up: return self.twiseUp()
		if dirr is direction.right: return self.twiseRight()
		if dirr is direction.down: return self.twiseDown()
		if dirr is direction.left: return self.twiseLeft()