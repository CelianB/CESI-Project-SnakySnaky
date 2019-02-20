# Florian Hervieux
import uuid

class Entity:
	def __init__(self, world):
		self.id = uuid.uuid4()
		self.world = world

	def getId(self):
		return self.id

	def assign(self, component):
		self.world._associate(self, component)

	def dissociate(self, component):
		self.world._dissociate(self, component)

	def get(self, component=None):
		if component:
			return self.world._getComponentForEntity(self, component)

