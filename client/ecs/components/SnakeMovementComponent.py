# Florian Hervieux
from .Component import Component
from util.snake_direction import SnakeDirection

class SnakeMovementComponent(Component):
	def __init__(self, direction: SnakeDirection=SnakeDirection.NONE):
		self.direction = direction

	def setDirection(self, direction):
		self.direction = direction

	def getDirection(self):
		return self.direction

	def getHeadRotation(self):
		if self.direction == SnakeDirection.UP:
			return 0
		elif self.direction == SnakeDirection.RIGHT:
			return 270
		elif self.direction == SnakeDirection.DOWN:
			return 180
		elif self.direction == SnakeDirection.LEFT:
			return 90

	def getRotation(self, beforeCase, currentCase):
		if beforeCase[0] > currentCase[0]:
			return 270
		elif beforeCase[0] < currentCase[0]:
			return 90
		elif beforeCase[1] > currentCase[1]:
			return 180
		elif beforeCase[1] < currentCase[1]:
			return 0