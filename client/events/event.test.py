from event_bus import EventBus
from sample_event import SampleEvent

KEY_ESCAPE = 27

event_bus = EventBus()
assert event_bus is not None

def onEventKey(event: SampleEvent):
	assert event is not None
	assert event.key == KEY_ESCAPE

assert len(event_bus.getHandlers(SampleEvent)) == 0

event_bus.unregister(onEventKey)
assert len(event_bus.getHandlers(SampleEvent)) == 0

event_bus.register(onEventKey)
assert len(event_bus.getHandlers(SampleEvent)) == 1

event_bus.unregister(onEventKey)
assert len(event_bus.getHandlers(SampleEvent)) == 0

event_bus.register(onEventKey)
assert len(event_bus.getHandlers(SampleEvent)) == 1

event_bus.emit(SampleEvent(KEY_ESCAPE))