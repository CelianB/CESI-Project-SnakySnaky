import sys
import pygame
from pygame.locals import *
from .events import EventBus, WindowCloseEvent

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
	def __init__(self, title, width, height, fps_target, **kwargs):
		pygame.init()
		self.frame = pygame.display.set_mode((width, height))
		pygame.display.set_caption(title)
		self.running = True
		self.input_manager = InputManager(self)
		self.fps_target = fps_target
		self.base_title = title
		self.event_bus = kwargs.get('event_bus', EventBus())

	def getBaseTitle(self):
		return self.base_title

	def getFrame(self):
		return self.frame

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

			# TODO: calculate delta time
			self.on_update(self.fps_target / 1000)

			# Clear frame
			self.frame.fill((0, 0, 0))
			self.on_render(self.frame)

			clock.tick(self.fps_target)
			pygame.display.update()

	def close(self):
		self.running = False
		self.event_bus.emit(WindowCloseEvent())
		pygame.quit()
		sys.exit()