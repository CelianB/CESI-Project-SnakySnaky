from event_bus import EventBus
from key_event import KeyEvent

KEY_ESCAPE = 27

event_bus = EventBus()
assert event_bus is not None

def onEventKey(event: KeyEvent):
	assert event is not None
	assert event.key == KEY_ESCAPE

assert len(event_bus.getHandlers(KeyEvent)) == 0

event_bus.unregister(onEventKey)
assert len(event_bus.getHandlers(KeyEvent)) == 0

event_bus.register(onEventKey)
assert len(event_bus.getHandlers(KeyEvent)) == 1

event_bus.unregister(onEventKey)
assert len(event_bus.getHandlers(KeyEvent)) == 0

event_bus.register(onEventKey)
assert len(event_bus.getHandlers(KeyEvent)) == 1

event_bus.emit(KeyEvent(KEY_ESCAPE))