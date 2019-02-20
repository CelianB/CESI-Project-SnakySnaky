#!/usr/bin/env python3
# -*- coding: utf-8 -*-5
# Florian Hervieux
from client.ecs.world import World
from client.ecs.components import Component, TransformComponent, GravityComponent
from vector2 import Vector2

deltaTime = 0.1

world = World()
assert world is not None
assert world.update is not None
assert world.all is not None
assert world.get is not None
assert world.cleanup is not None

ent = world.createEntity()
assert ent is not None

ent2 = world.createEntity()
assert ent2 is not None

ent3 = world.createEntity()
assert ent3 is not None

entId = ent.getId()
assert entId is not None

c1 = TransformComponent(Vector2(10, 4), Vector2(0, 0), Vector2(1, 1))
c2 = GravityComponent(9.81)
assert c1 is not None
assert c2 is not None
assert isinstance(c1, Component)
assert isinstance(c1, TransformComponent)
assert isinstance(c2, Component)
assert isinstance(c2, GravityComponent)
ent.assign(c1)
ent.assign(c2)

c12 = TransformComponent(Vector2(3, 27), Vector2(32, 5), Vector2(1.5, 1.5))
c22 = GravityComponent(6.34)
ent2.assign(c12)
ent2.assign(c22)

assert ent.get(TransformComponent) is not None
assert ent.get(GravityComponent) is not None
assert ent2.get(TransformComponent) is not None
assert ent2.get(GravityComponent) is not None

print()

def onAll(entity):
	print(entity.getId())
world.all(onAll)

def onEach(entity, transform, gravity):
	print()
	print(entity.getId())
	print(transform.getPosition())
	print(gravity.getForce())
	beforeY = transform.getPosition().y
	transform.getPosition().y += gravity.getForce() * deltaTime
	afterY = transform.getPosition().y
	print(afterY)
	assert beforeY != afterY
world.get(onEach, components=[TransformComponent, GravityComponent])

# ent2.dissociate(GravityComponent)
# assert ent2.get(GravityComponent) is None

print()

world.cleanup()
