import collections
import random

from event_bus.bus import UntypedEventBus


class API:
    def __init__(self, emitter):
        self.emitter = emitter

    def post(self):
        self.emitter("api_call", "API POST call data")
        self.emitter("security_event", "POST")

    def put(self):
        self.emitter("api_call", "API PUT call data")
        self.emitter("security_event", "PUT")

    def get(self):
        self.emitter("api_call", "API GET call data")

    def delete(self):
        self.emitter("api_call", "API DELETE call data")
        self.emitter("security_event", "DELETE")

    def patch(self):
        self.emitter("api_call", "API PATCH call data")
        self.emitter("security_event", "PATCH")

    def option(self):
        self.emitter("api_call", "API OPTION call data")
        self.emitter("security_event", "OPTION")


def closure_security_event_handler(emitter, counter: collections.Counter):
    """
    This function creates a closure with access to the counter created within the outer function and the emitter passed
    in as an argument
    :param counter: for tracking the amount of times a security event occurs throughout the entire application
    :param emitter: emitter used by the handler to raise additional events
    :return: security event handler
    """

    def handler(data):
        """
        A handler for security events. This handler has access to the outer function's counter and emitter.
        :param data: data emitted from an event
        """
        # Do something security relevant
        counter[data] += 1
        emitter("log_event", f"security event occurred: {data}")

    return handler


def log_event_handler(data):
    """
    A simple event handler that does not involve closures
    :param data:
    :return:
    """
    # Do logging things
    print(data)


def closure_api_call_handler(emitter):
    """
    This function creates a closure with access to the emitter passed in as an argument
    :param emitter: emitter used by the handler to raise additional events
    :return: api call handler
    """

    def handler(data):
        # Data could be a request/response object
        # Do things here for validation, etc
        # We emit a log event to simulate logging request/response data
        emitter("log_event", data)

    return handler


def main():
    bus = UntypedEventBus()
    counter = collections.Counter()
    bus.register("security_event", closure_security_event_handler(bus.emit, counter))
    bus.register("log_event", log_event_handler)
    bus.register("api_call", closure_api_call_handler(bus.emit))

    # logic
    api_client = API(bus.emit)
    calls=[
        api_client.get,
        api_client.put,
        api_client.post,
        api_client.delete,
        api_client.option
    ]
    i = 0
    while i < 100:
        random.choice(calls)()
        i += 1
    bus.emit("log_event", counter)


if __name__ == '__main__':
    main()
