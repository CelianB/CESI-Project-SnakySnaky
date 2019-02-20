# Florian Hervieux
from .System import System
from client.ecs.components import TransformComponent, TerrainComponent

class SnakeMovementSystem(System):
	def __init__(self, world, graphics, cell_size):
		self.world = world
		self.graphics = graphics
		self.cell_size = cell_size

	def onEachTerrain(self, entity, transform_cmp, terrain_cmp):
		w, h = self.cell_size
		# Loop over rows.
		for idx_r, row in enumerate(terrain_cmp.layer_ground):
			# Loop over columns.
			for idx_c, column in enumerate(row):
				self.graphics.drawImage(terrain_cmp.getGroundSprite(column), (transform_cmp.getPosition().x + idx_c * w, transform_cmp.getPosition().y + idx_r * h))

	def run(self):
		self.world.get(self.onEachTerrain, components=[TransformComponent, TerrainComponent])