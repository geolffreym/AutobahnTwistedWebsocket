__author__ = 'gmena'
from inspect import isfunction
from autobahn.twisted.websocket import \
    WebSocketClientProtocol, WebSocketClientFactory
from autobahn.websocket.http import HttpException
from twisted.internet import reactor


class WebSocketClient(WebSocketClientProtocol):
    """"The Protocol Factory"""

    def __init__(self, EventObject):
        self.events = EventObject

    def __call__(self, *args, **kwargs):
        return self

    def onConnect(self, response):
        """On Connect what to do?"""
        if self.events.on_connect is not None:
            self.events.on_connect(response)

    def onOpen(self):
        """On Open what to do?"""
        if self.events.on_open is not None:
            self.events.on_open(self)

    def onMessage(self, payload, isBinary):
        """On Message what to do?"""
        if self.events.on_message is not None:
            self.events.on_message(payload)

    def onClose(self, wasClean, code, reason):
        """On Close what to do?"""
        if self.events.on_close is not None:
            self.events.on_close(code, reason)


class MiddleWareSocketEvent(object):
    """""A MiddleWare Event Class"""

    def __init__(self):
        self.on_connect = None
        self.on_open = None
        self.on_close = None
        self.on_message = None

    def set_on_connect(self, callback):
        """
        Set callback event for connect event
        @:param callback function
        """
        if isfunction(callback):
            self.on_connect = callback

    def set_on_open(self, callback):
        """
        Set callback event for open event
        @:param callback function
        """
        if isfunction(callback):
            self.on_open = callback

    def set_on_clone(self, callback):
        """
        Set callback event for close event
        @:param callback function
        """
        if isfunction(callback):
            self.on_close = callback

    def set_on_message(self, callback):
        """
        Set callback event for message event
        @:param callback function
        """
        if isfunction(callback):
            self.on_message = callback


class SocketMiddleWare(MiddleWareSocketEvent):
    def connect_socket(self, user, port=8000):
        """
        Connect the client to server
        @:param user string
        @:param port int
        """
        factory = WebSocketClientFactory("ws://localhost:" + str(port) + "?user=" + user, debug=False)
        factory.protocol = WebSocketClient(self)

        reactor.connectTCP('127.0.0.1', port, factory)
        reactor.run()

        return factory.protocol


# Example
def connect(response):
    print "I am connected callback"


socket = SocketMiddleWare()
socket.set_on_connect(connect)
socket.connect_socket('Juan')

