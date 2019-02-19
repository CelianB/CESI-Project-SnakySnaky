from .Component import Component

class TerrainComponent(Component):
	def __init__(self, cols, rows):
		self.array = [[0] * cols] * rows