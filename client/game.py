from pygame.locals import *
from .ecs.world import World
from .game_states import GameStates

class Game:
	def __init__(self, window):
		self.window = window
		self.world = World()
		self.game_state = GameStates.IN_GAME

	def on_input(self, event):
		if event.type == QUIT:
			self.window.close()

	def on_update(self, deltaTime):
		pass

	def on_render(self, graphics):
		pass