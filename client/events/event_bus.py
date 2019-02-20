class EventBus:
	def __init__(self):
		self.mapping = {}

	def register(self, handler):
		clazz = handler.__annotations__[list(handler.__annotations__)[0]]
		if not clazz in self.mapping:
			self.mapping[clazz] = []
		self.mapping[clazz].append(handler)

	def unregister(self, handler):
		clazz = handler.__annotations__[list(handler.__annotations__)[0]]
		if clazz in self.mapping:
			self.mapping[clazz].remove(handler)

	def getHandlers(self, event_class):
		if event_class in self.mapping:
			return self.mapping[event_class]
		else:
			return []

	def emit(self, event):
		handlers = self.mapping[event.__class__]
		if handlers:
			for h in handlers:
				h(event)