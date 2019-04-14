# Florian Hervieux
# Célian Bastien
import pygame
import socket
import json
import select

from pygame.locals import *
from client.ecs.world import World
from client.ecs.components import TransformComponent, TerrainComponent, SpriteRendererComponent, SnakeMovementComponent, SnakeBehaviourComponent, ItemComponent
from client.ecs.systems import SystemTypes, TerrainSystem
from client.game_states import GameStates
from util.vector2 import Vector2
from client.graphics import Graphics
from util import SnakeDirection, ItemType
from client.networking import Networking
from protocolSerialization import ProtocolSerialization
from types import SimpleNamespace as Namespace

waitingTab = ['', '.', '..', '...']
waitingIndex = 0

snake_speed = 1
cell_size = (16, 16)

class Game:
	def __init__(self, window, event_bus, map_size):
		global myfont
		global testFont
		self.window = window
		self.world = World()

		self.event_bus = event_bus
		self.networking = Networking(event_bus)
		self.protocolSerialization = ProtocolSerialization()

		self.updates = 0
		self.updates_wainting = 0
		testFont = pygame.font.Font('assets/fonts/Roboto-Medium.ttf', 38)

		# windows creation
		self.graphics = Graphics(window.getBaseTitle(), window.getFrame())
		# bus event handler
		self.event_bus = event_bus

		self.game_state = GameStates.WAITING_ROOM

		self.other_snakes = []
		if(self.networking.started == True):
			self.game_state = GameStates.IN_GAME
			self.networking.send(self.protocolSerialization.ClientStartMessage(self.networking.id))
			initialPosition = json.loads(self.networking.s.recv(1024),object_hook=lambda d: Namespace(**d))
			# snake entity creation
			self.snake = self.world.createEntity(Vector2(20, 20))
			self.snake.assign(SpriteRendererComponent(self.graphics, 'mini_snake.png'))
			self.snake.assign(SnakeMovementComponent(SnakeDirection.LEFT))
			self.snake.assign(SnakeBehaviourComponent(self.graphics,initialPosition.position,initialPosition.direction))
			mySnakeBehave = self.snake.get(SnakeBehaviourComponent)
			mySnakeMovement = self.snake.get(SnakeMovementComponent)
			for x in range(0, 7):
				mySnakeBehave.growUp(mySnakeMovement.getDirection())

			# background entity creation
			terrain = self.world.createEntity(Vector2(0, 0), Vector2(), Vector2(1, 1))
			terrain.assign(TerrainComponent(self.graphics, map_size, map_size))
			terrain_system = self.world.createSystem(SystemTypes.RENDER, TerrainSystem(self.world, self.graphics, cell_size), 1)
			# snake_movement_system = self.world.createSystem(SystemTypes.UPDATE, SnakeMovementSystem())

			# Bunny creation
			bunny = self.world.createEntity(Vector2(30, 30))
			bunny.assign(ItemComponent(ItemType.BUNNY))
			bunny.assign(SpriteRendererComponent(self.graphics, 'rabbit.png'))

			# Mine creation
			mine = self.world.createEntity(Vector2(40, 40))
			mine.assign(ItemComponent(ItemType.MINE))
			mine.assign(SpriteRendererComponent(self.graphics, 'mine.png'))

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

	def processUpdate(self,snakes):
		snakes = json.loads(snakes,object_hook=lambda d: Namespace(**d))
		for snake in snakes:
			if(snake.id == self.networking.id):
				if(snake.alive == False):
					self.game_state = GameStates.DEAD
			else:
				ind = 0
				for otherSnake in self.other_snakes:
					if(snake.id == otherSnake["id"]):
						del self.other_snakes[ind]
					ind = ind + 1
				self.other_snakes.append({"id":snake.id,"position":snake.position,"direction":snake.direction,"score":snake.score})

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
			elif event.key in [K_KP_PLUS, K_KP_MINUS, K_KP_ENTER]:
				snake_behaviour = self.snake.get(SnakeBehaviourComponent)
				if event.key == K_KP_PLUS:
					snake_movement = self.snake.get(SnakeMovementComponent)
					snake_behaviour.growUp(snake_movement.getDirection())
				elif event.key == K_KP_MINUS:
					snake_behaviour.removeLast()
				elif event.key == K_KP_ENTER:
					self.game_state = GameStates.DEAD

	def on_update(self, deltaTime):
		self.updates += deltaTime

		if self.game_state == GameStates.WAITING_ROOM:
			global waitingIndex
			global waitingTab
			self.updates_wainting += deltaTime
			if self.updates_wainting > 0.1:
				self.updates_wainting = 0
				if waitingIndex >= len(waitingTab) - 1:
					waitingIndex = 0
				else:
					waitingIndex += 1

		elif self.game_state == GameStates.IN_GAME:
			self.world.update(SystemTypes.UPDATE)
			def onEachSnakeMovement(entity, transform_cmp, snake_movement_cmp, behaviour_cmp):
				dirs = {
					SnakeDirection.UP: self.snakeGoUp,
					SnakeDirection.DOWN: self.snakeGoDown,
					SnakeDirection.LEFT: self.snakeGoLeft,
					SnakeDirection.RIGHT: self.snakeGoRight,
				}
				if snake_movement_cmp.getDirection() in dirs:
					dirs[snake_movement_cmp.getDirection()](transform_cmp.getPosition(), snake_movement_cmp)
					self.networking.send(self.protocolSerialization.ClientMoveMessage(self.networking.id,behaviour_cmp.position,snake_movement_cmp.getDirection().value))
					behaviour_cmp.update(snake_movement_cmp.getDirection())
					connexions_request, wlist, xlist = select.select([self.networking.s],[], [], 0.05)	
					for connexion in connexions_request:
						data = connexion.recv(1024).decode()
						if(data != ''):
							self.processUpdate(data)

			self.world.get(onEachSnakeMovement, components=[TransformComponent, SnakeMovementComponent, SnakeBehaviourComponent])

	def on_render(self, frame):
		if self.game_state == GameStates.WAITING_ROOM:
			global waitingIndex
			global waitingTab
			global testFont
			text = "Waiting" + waitingTab[waitingIndex]
			rect = self.graphics.drawCenteredText(testFont, text, (0, 0, 0), frame.get_height() / 2 - testFont.get_height() / 2, False)
			self.graphics.drawText3D(testFont, text, (140, 140, 140), (255, 255, 255), rect.topleft)

		elif self.game_state == GameStates.IN_GAME:
			self.world.update(SystemTypes.RENDER)

			def drawSnake(positions,direction,behaviour):
				for i, pos in enumerate(positions):
					if i == 0:
						img = 'head' if (len(positions) != 1) else 'mini_snake'
						r = direction.getHeadRotation()
					else:
						r = direction.getRotation(positions[i - 1], positions[i])
						if i == len(positions) - 1:
							img = 'tail'
						else:
							nextR = direction.getRotation(positions[i], positions[i + 1])
							oldVertical = True if (nextR == 0 or nextR == 180) else False
							vertical = True if (r == 0 or r == 180) else False

							if oldVertical != vertical:
								img = 'corner_left_top'
								if (nextR == 0 and r == 90) or (r == 180 and nextR == 270):
									r = 90
								if (r == 0 and nextR == 90) or (nextR == 180 and r == 270):
									r = 270
								if (nextR == 0 and r == 270) or (r == 180 and nextR == 90):
									r = 180
								if (r == 0 and nextR == 270) or (nextR == 180 and r == 90):
									r = 0
							else:
								img = 'straight'
					if r is not None:
						self.graphics.drawImage(self.graphics.rotateImage(behaviour.sprites[img], r), (pos[0] * cell_size[0], pos[1] * cell_size[1]))

			def onEachSpriteRenderer(entity, transform_cmp, movement_cmp, behaviour_cmp, sprite_renderer_com):
				drawSnake(behaviour_cmp.position,movement_cmp,behaviour_cmp)
			self.world.get(onEachSpriteRenderer, components=[TransformComponent, SnakeMovementComponent, SnakeBehaviourComponent, SpriteRendererComponent])
			
			for otherSnake in self.other_snakes :
				direction = SnakeMovementComponent(otherSnake['direction'])
				behaviour = SnakeBehaviourComponent(self.graphics,otherSnake['position'],otherSnake['direction'])
				drawSnake(otherSnake['position'],direction,behaviour)

			def onEachItemRenderer(entity, transform_cmp, sprite_renderer_com, item_cmp):
				x, y = transform_cmp.getPosition()
				self.graphics.drawImage(sprite_renderer_com.getImage(), (x * cell_size[0], y * cell_size[1]))
			self.world.get(onEachItemRenderer, components=[TransformComponent, SpriteRendererComponent, ItemComponent])

		elif self.game_state == GameStates.DEAD:
			text = "You are dead!"
			rect = self.graphics.drawCenteredText(testFont, text, (0, 0, 0), frame.get_height() / 2 - testFont.get_height() / 2, False)
			self.graphics.drawText3D(testFont, text, (140, 140, 140), (255, 255, 255), rect.topleft)
			