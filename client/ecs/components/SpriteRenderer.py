import pygame
from multipledispatch import dispatch
from client.graphics import Graphics
from .Component import Component

class SpriteRenderer(Component):
	@dispatch(Graphics, str)
	def __init__(self, graphics, image):
		self.image = graphics.loadImage(image)

	@dispatch(pygame.Surface)
	def __init__(self, image):
		self.image = image

	def getImage(self):
		return self.image