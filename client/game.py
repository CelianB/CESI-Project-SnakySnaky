import pygame
from pygame.locals import *
from client.ecs.world import World
from client.ecs.components import TransformComponent, TerrainComponent
from client.game_states import GameStates
from util.vector2 import Vector2
from client.graphics import Graphics

waitingTab = ['', '.', '..', '...']
waitingIndex = 0

class Game:
	def __init__(self, window):
		global myfont
		global testFont
		global grass_img
		self.window = window
		self.world = World()
		self.game_state = GameStates.IN_GAME
		self.updates = 0
		self.updates_wainting = 0
		testFont = pygame.font.Font('assets/fonts/test.ttf', 24)

		self.graphics = Graphics(window.getBaseTitle(), window.getFrame())
		grass_img = self.graphics.loadImage('grass.png')

		terrain = self.world.createEntity(Vector2(0, 0), Vector2(), Vector2())
		terrain.assign(TerrainComponent(60, 60))

	def on_input(self, event):
		if event.type == QUIT:
			self.window.close()

	def on_update(self, deltaTime):
		self.updates += deltaTime

		if self.game_state == GameStates.WAITING_ROOM:
			global waitingIndex
			global waitingTab
			self.updates_wainting += deltaTime
			if self.updates_wainting > 0.4:
				self.updates_wainting = 0
				if waitingIndex >= len(waitingTab) - 1:
					waitingIndex = 0
				else:
					waitingIndex += 1

		elif self.game_state == GameStates.IN_GAME:
			pass

	def on_render(self, frame):
		if self.game_state == GameStates.WAITING_ROOM:
			global waitingIndex
			global waitingTab
			global testFont
			label = testFont.render('Waiting' + waitingTab[waitingIndex], 1, (255,255,255))
			frame.blit(label, (100, 100))

		elif self.game_state == GameStates.IN_GAME:
			def onEach(entity, transform_comp, terrain_comp):
				w, h = grass_img.get_size()
				# Loop over rows.
				for idx_r, row in enumerate(terrain_comp.array):
					# Loop over columns.
					for idx_c, column in enumerate(row):
						self.graphics.drawImage(grass_img, (idx_c * w, idx_r * h))
			self.world.get(onEach, components=[TransformComponent, TerrainComponent])