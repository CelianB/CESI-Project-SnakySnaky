from .entity import Entity

class World:
	def __init__(self):
		print('World')
		# ? entity_id => component[]
		self.entity_to_components = {} # entity => component[]
		# ? component_class => entity_id[]
		self.component_to_entities = {} # component_class => entity[]
		self.entities = {} # entity_id => entity

	def createEntity(self):
		print('World:createEntity')
		entity = Entity(self)
		self.entity_to_components[entity] = []
		return entity

	def update(self):
		# foreach systems
		print('World:update')

	def get(self, func, **kwargs):
		components = kwargs.get('components', None)
		if components:
			for entity, entity_components in self.entity_to_components.items():
				args = []
				flag = True
				for c in components:
					result = None
					for elem in entity_components:
						if isinstance(elem, c):
							result = elem
							break
					if result:
						args.append(result)
						if len(args) == len(components):
							break
					else:
						flag = False
						break
				if flag:
					func(entity, *args)

	def all(self, func):
		for e in self.entity_to_components.keys():
			func(e)

	def _associate(self, entity, component):
		component_clz = component.__class__

		if not component_clz in self.component_to_entities:
			self.component_to_entities[component_clz] = []

		self.entity_to_components[entity].append(component)
		self.component_to_entities[component_clz].append(entity)

	def _dissociate(self, entity, component_clz):
		# TODO: Check this
		print('Remove', component_clz, 'from', entity)
		self.entity_to_components[entity] = list(filter(lambda x: x.__class__ != component_clz, self.entity_to_components[entity]))
		self.component_to_entities[component_clz] = list(filter(lambda x: x.getId() != entity.getId(), self.component_to_entities[component_clz]))
		print()
		print(entity)
		print(self.component_to_entities[component_clz])
		print()
		pass

	def _getComponentForEntity(self, entity, component):
		components = self.entity_to_components[entity]
		if components:
			filtered = filter(lambda x: x.__class__ == component.__class__, components)
			return filtered

	def delete(self, entity):
		for c in self.entity_to_components[entity]:
			if c.__class__ in self.component_to_entities:
				arr = self.component_to_entities[c.__class__]
				arr.remove(entity)
		del self.entity_to_components[entity]
		del self.entities[entity.getId()]

	def cleanup(self):
		print('World:cleanup')
		self.entity_to_components = {}
		self.component_to_entities = {}
		self.entities = {}