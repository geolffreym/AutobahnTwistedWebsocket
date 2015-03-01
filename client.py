__author__ = 'gmena'
from inspect import isfunction
from autobahn.twisted.websocket import \
    WebSocketClientProtocol, WebSocketClientFactory
from autobahn.websocket.http import HttpException
from multiprocessing import Process
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
            callback = self.events.on_connect.pop('callback')
            print callback
            callback(response=response, peer=self, params=self.events.on_connect)

    def onOpen(self):
        """On Open what to do?"""
        if self.events.on_open is not None:
            callback = self.events.on_open.pop('callback')
            callback(peer=self, params=self.events.on_open)

    def onMessage(self, payload, isBinary):
        """On Message what to do?"""
        if self.events.on_message is not None:
            callback = self.events.on_message.pop('callback')
            callback(message=payload, peer=self, params=self.events.on_message)

    def onClose(self, wasClean, code, reason):
        """On Close what to do?"""
        if self.events.on_close is not None:
            callback = self.events.on_close.pop('callback')
            callback(peer=self, code=code, reason=reason, params=self.events.on_close)


class MiddleWareSocketEvent(object):
    """""A MiddleWare Event Class"""

    def __init__(self):
        self.on_connect = None
        self.on_open = None
        self.on_close = None
        self.on_message = None
        self.peer = None

    def set_on_connect(self, *args, **kwargs):
        if 'callback' in kwargs:
            if isfunction(kwargs.get('callback')):
                self.on_connect = kwargs

    def set_on_open(self, *args, **kwargs):
        if 'callback' in kwargs:
            if isfunction(kwargs.get('callback')):
                self.on_open = kwargs

    def set_on_close(self, *args, **kwargs):
        if 'callback' in kwargs:
            if isfunction(kwargs.get('callback')):
                self.on_close = kwargs

    def set_on_message(self, *args, **kwargs):
        if 'callback' in kwargs:
            if isfunction(kwargs.get('callback')):
                self.on_message = kwargs


class SocketMiddleWare(MiddleWareSocketEvent):
    def connect_socket(self, user='default', port=9000):
        factory = WebSocketClientFactory("ws://localhost:" + str(port) + "?user=" + str(user), debug=False)
        self.peer = factory.protocol = WebSocketClient(self)

        reactor.connectTCP('127.0.0.1', port, factory)
        reactor.run()

    def async_connect(self, user='default', port=9000):
        websocket_process = Process(target=self.connect_socket, name='websocket_client', args=(user, port))
        websocket_process.start()

        return websocket_process

    def get_peer(self):
        return self.peer


# Example
def message(*args, **kwargs):
    print message


def connect(*args, **kwargs):
    print "I am connected callback"


socket = SocketMiddleWare()

# Event Handlers
socket.set_on_connect(callback=connect)
socket.set_on_message(callback=message)

# Run client
socket.async_connect('Juan')



