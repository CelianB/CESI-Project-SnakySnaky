import sys
import pygame
from pygame.locals import *

def null_function():
	pass

class InputManager:
	def __init__(self, window):
		self.window = window

	def resetMouse(self):
		self.isMouseLeftDown = False
		self.isMouseRightDown = False
		self.isMouseMiddleDown = False

class Window:
	def __init__(self, title, width, height, fps_target):
		pygame.init()
		self.frame = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
		self.running = True
		self.input_manager = InputManager(self)
		self.fps_target = fps_target

	def _default_input(self, event):
		if event.type == QUIT:
			self.close()

	def run(self, **kwargs):
		self.on_input = kwargs.get('input', self._default_input)
		if self._default_input is None:
			self.on_input = self._default_input
		self.on_update = kwargs.get('update', null_function)
		self.on_render = kwargs.get('render', null_function)
		self._update()

	def _update(self):
		clock = pygame.time.Clock()

		while self.running:
			self.input_manager.resetMouse()

			for event in pygame.event.get():
				self.on_input(event)

			self.on_update()

			# Clear frame
			self.frame.fill((0, 0, 0))
			self.on_render()

			clock.tick(self.fps_target)
			pygame.display.update()

	def close(self):
		self.running = False
		pygame.quit()
		sys.exit()