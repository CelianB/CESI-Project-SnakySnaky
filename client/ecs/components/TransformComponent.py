from .Component import Component

class TransformComponent(Component):
	def __init__(self, position, rotation, scale):
		self.position = position
		self.rotation = rotation
		self.scale = scale

	def getPosition(self):
		return self.position

	def getRotation(self):
		return self.rotation

	def getScale(self):
		return self.scale