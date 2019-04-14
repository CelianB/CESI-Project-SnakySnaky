# Florian Hervieux
from .Component import Component
from util.snake_direction import SnakeDirection

class SnakeBehaviourComponent(Component):
	def __init__(self, graphics, position, direction):
		self.position = [position]

		self.sprites = {
			'corner_left_top'  : graphics.loadImage('corner_left_top.png'),
			'corner_right_top' : graphics.loadImage('corner_right_top.png'),
			'half_turn'        : graphics.loadImage('half_turn.png'),
			'head'             : graphics.loadImage('head.png'),
			'tail'             : graphics.loadImage('tail.png'),
			'mini_snake'       : graphics.loadImage('mini_snake.png'),
			'straight'         : graphics.loadImage('straight.png'),
		}

	def addLength(self, direction):
		newpos = self.position[0][:]

		if direction == SnakeDirection.UP:
			newpos[1] -= 1
		elif direction == SnakeDirection.RIGHT:
			newpos[0] += 1
		elif direction == SnakeDirection.DOWN:
			newpos[1] += 1
		elif direction == SnakeDirection.LEFT:
			newpos[0] -= 1

		# We insert item at first pos in array
		self.position.insert(0, newpos)

	def removeLast(self):
		# We remove the last item if there is more than one
		if len(self.position) > 1:
			self.position.pop()

	def growUp(self,direction):
		newpos = self.position[-1][:]
		if direction == SnakeDirection.UP.value:
			newpos[1] += 1
		elif direction == SnakeDirection.RIGHT.value:
			newpos[0] -= 1
		elif direction == SnakeDirection.DOWN.value:
			newpos[1] -= 1
		elif direction == SnakeDirection.LEFT.value:
			newpos[0] += 1

		# We insert item at first pos in array
		self.position.append(newpos)


	def update(self, direction):
		self.addLength(direction)
		self.removeLast()