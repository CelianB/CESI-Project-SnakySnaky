import pygame
from pygame.locals import *
from client.ecs.world import World
from client.ecs.components import TransformComponent, TerrainComponent, SpriteRenderer, SnakeMovementComponent, SnakeBehaviourComponent
from client.game_states import GameStates
from util.vector2 import Vector2
from client.graphics import Graphics
from util.snake_direction import SnakeDirection

waitingTab = ['', '.', '..', '...']
waitingIndex = 0

snake_speed = 1
cell_size = (16, 16)

class Game:
	def __init__(self, window):
		global myfont
		global testFont
		self.window = window
		self.world = World()
		self.game_state = GameStates.IN_GAME
		self.updates = 0
		self.updates_wainting = 0
		testFont = pygame.font.Font('assets/fonts/test.ttf', 24)

		self.graphics = Graphics(window.getBaseTitle(), window.getFrame())

		terrain = self.world.createEntity(Vector2(0, 0), Vector2(), Vector2(1, 1))
		terrain.assign(TerrainComponent(self.graphics, 60, 60))

		self.snake = self.world.createEntity(Vector2(20, 20))
		self.snake.assign(SpriteRenderer(self.graphics, 'mini_snake.png'))
		self.snake.assign(SnakeMovementComponent())
		self.snake.assign(SnakeBehaviourComponent(self.graphics))

	def snakeGoUp(self, snake_position, snake_movement):
		snake_position.y -= snake_speed * cell_size[1]
		snake_movement.setDirection(SnakeDirection.UP)

	def snakeGoDown(self, snake_position, snake_movement):
		snake_position.y += snake_speed * cell_size[1]
		snake_movement.setDirection(SnakeDirection.DOWN)

	def snakeGoLeft(self, snake_position, snake_movement):
		snake_position.x -= snake_speed * cell_size[0]
		snake_movement.setDirection(SnakeDirection.LEFT)

	def snakeGoRight(self, snake_position, snake_movement):
		snake_position.x += snake_speed * cell_size[0]
		snake_movement.setDirection(SnakeDirection.RIGHT)

	def on_input(self, event):
		if event.type == QUIT:
			self.window.close()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				self.window.close()
			elif event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
				snake_position = self.snake.get(TransformComponent).getPosition()
				snake_movement = self.snake.get(SnakeMovementComponent)
				if event.key == K_UP:
					self.snakeGoUp(snake_position, snake_movement)
				elif event.key == K_DOWN:
					self.snakeGoDown(snake_position, snake_movement)
				elif event.key == K_LEFT:
					self.snakeGoLeft(snake_position, snake_movement)
				elif event.key == K_RIGHT:
					self.snakeGoRight(snake_position, snake_movement)

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
			def onEachSnakeMovement(entity, transform_cmp, snake_movement_cmp, behaviour_cmp):
				dirs = {
					SnakeDirection.UP: self.snakeGoUp,
					SnakeDirection.DOWN: self.snakeGoDown,
					SnakeDirection.LEFT: self.snakeGoLeft,
					SnakeDirection.RIGHT: self.snakeGoRight,
				}
				if snake_movement_cmp.getDirection() in dirs:
					dirs[snake_movement_cmp.getDirection()](transform_cmp.getPosition(), snake_movement_cmp)
					behaviour_cmp.update(snake_movement_cmp.getDirection())
			self.world.get(onEachSnakeMovement, components=[TransformComponent, SnakeMovementComponent, SnakeBehaviourComponent])

	def on_render(self, frame):
		if self.game_state == GameStates.WAITING_ROOM:
			global waitingIndex
			global waitingTab
			global testFont
			label = testFont.render('Waiting' + waitingTab[waitingIndex], 1, (255,255,255))
			frame.blit(label, (100, 100))

		elif self.game_state == GameStates.IN_GAME:
			def onEachTerrain(entity, transform_cmp, terrain_cmp):
				w, h = cell_size
				# Loop over rows.
				for idx_r, row in enumerate(terrain_cmp.array):
					# Loop over columns.
					for idx_c, column in enumerate(row):
						self.graphics.drawImage(terrain_cmp.getSprite(column), (transform_cmp.getPosition().x + idx_c * w, transform_cmp.getPosition().y + idx_r * h))
			self.world.get(onEachTerrain, components=[TransformComponent, TerrainComponent])

			def onEachSpriteRenderer(entity, transform_cmp, movement_cmp, behaviour_cmp, sprite_renderer_com):
				# self.graphics.drawImage(sprite_renderer_cmp.getImage(), (transform_cmp.getPosition().x, transform_cmp.getPosition().y))
				for i, pos in enumerate(behaviour_cmp.position):
					if i == 0:
						img = 'head' if (len(behaviour_cmp.position) != 1) else 'mini_snake'
						r = movement_cmp.getHeadRotation()
					else:
						r = movement_cmp.getRotation(behaviour_cmp.position[i-1], behaviour_cmp.position[i])
						if i == len(behaviour_cmp.position):
							img = 'tail'
						else:
							img = 'straight'
					if r is not None:
						self.graphics.drawImage(self.graphics.rotateImage(behaviour_cmp.sprites[img], r), (pos[0] * cell_size[0], pos[1] * cell_size[1]))
			self.world.get(onEachSpriteRenderer, components=[TransformComponent, SnakeMovementComponent, SnakeBehaviourComponent, SpriteRenderer])