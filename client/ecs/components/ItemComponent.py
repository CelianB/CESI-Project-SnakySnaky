from .Component import Component
from util.item_type import ItemType

class ItemComponent(Component):
	def __init__(self, item_type: ItemType):
		self.item_type = item_type

	def getType(self):
		return self.item_type