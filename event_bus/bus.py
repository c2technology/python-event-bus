import dataclasses
from typing import Callable, Awaitable, Optional, Any


@dataclasses.dataclass
class EventData:
    """
    Convenience typing for a dict to imply it is used in event handling.
    """
    name: str


class EventHandler:
    """
    Event Handlers are a callable function that takes EventData and returns nothing: (EventData) -> None
    The EventHandler implementation can be a function on an object or a standalone function. Closures should be used if
    internal data is used when handling an event
    """
    handler: Callable[[EventData], Awaitable[None]]



class TypedEventBus:
    """
    An Event Bus allows different Event Handlers to register themselves to a specific event. When that event is emitted
    using the EventBus, any registered Handlers are invoked with data presented at emission time.
    """

    def __init__(self):
        self.registry = {}
        self.event_handlers = dict()


    def register(self, event_name: str, func: EventHandler):
        """
        Registers an EventHandler for a given event_name. This handler will be called each time the event_name is emitted.
        :param event_name: The name of the event to register
        :param func: EventHandler for the given event_name
        """
        if not self.registry.get(event_name, None):
            self.registry[event_name] = {func}
        else:
            self.registry[event_name].add(func)

    def unregister(self, event_name, event_handler: EventHandler):
        """
        Unregisters an EventHandler from an event_name, if registered. If the event is not registered, nothing happens.
        :param event_name: The event name to unregister
        :param event_handler: The EventHandler to unregister
        """
        self.registry[event_name].remove(event_handler)
        if len(self.registry[event_name]) == 0:
            del self.registry[event_name]

    def emit(self, event_name, data: EventData):
        """
        Calls all EventHandlers registerd with the given EventName. Each EventHandler is passed the EventData, which may
        contain different data for each Event. If no EventHandlers are registered for the event_name, nothing happens.
        :param event_name: The event name to invoke
        :param data: The EventData to send
        """
        event_handlers = self.registry.get(event_name, [])
        for event_handler in event_handlers:
            event_handler(event_name, data)


class UntypedEventBus:
    """
    An Event Bus allows different Event Handlers to register themselves to a specific event. When that event is emitted
    using the EventBus, any registered Handlers are invoked with data presented at emission time.
    """
    def __init__(self):
        self.registry = {}

    def register(self, event_name: str, event_handler: Callable[[Any], None]):
        """
        Registers an EventHandler for a given event_name. This handler will be called each time the event_name is emitted.
        :param event_name: The name of the event to register
        :param event_handler: EventHandler for the given event_name
        """
        if not self.registry.get(event_name, None):
            self.registry[event_name] = {event_handler}
        else:
            self.registry[event_name].add(event_handler)

    def unregister(self, event_name, event_handler: Callable[[Any], None]):
        """
        Unregisters an EventHandler from an event_name, if registered. If the event is not registered, nothing happens.
        :param event_name: The event name to unregister
        :param event_handler: The EventHandler to unregister
        """
        self.registry[event_name].remove(event_handler)
        if len(self.registry[event_name]) == 0:
            del self.registry[event_name]

    def emit(self, event_name, data: Optional[dict] = None):
        """
        Calls all EventHandlers registered with the given EventName. Each EventHandler is passed the EventData, which
        may contain different data for each Event. If no EventHandlers are registered for the event_name, nothing
        happens.
        :param event_name: The event name to invoke
        :param data: The EventData to send
        """
        event_handlers = self.registry.get(event_name, [])
        for event_handler in event_handlers:
            event_handler(data)

