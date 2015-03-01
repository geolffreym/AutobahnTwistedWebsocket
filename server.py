from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
from autobahn.websocket.http import HttpException
from twisted.internet import reactor
from multiprocessing import Process
import json


class WebSocket(WebSocketServerProtocol):
    """
    WebSocketProtocol
    http://autobahn.ws/python/reference/autobahn.websocket.html#autobahn.websocket.protocol.WebSocketServerProtocol.onConnect
    """

    def __init__(self, dclients):
        self.clients = dclients
        self.client = None
        self.peer = None

    def __call__(self, *args, **kwargs):
        return self

    def onConnect(self, request):

        # Who can connect to my server?
        if not request.origin == "http://127.0.0.1:8000":
            raise HttpException(401, "Not authorized user")

        # Live client and Peer
        self.client = request.params.get('user')[0]
        self.peer = request.peer
        print "Connected"

    def onOpen(self):
        user = self.client
        self.clients[user] = self
        print "Connection Open for " + user

    def onMessage(self, payload, isBinary):
        # On Message just Handle
        print "New Message. Handling..."
        self.handleMessage(payload)

    def onClose(self, wasClean, code, reason):
        if self.client in clients:
            del clients[self.client]
        print "Connection Closed"

    def sendBack(self, message):
        """Send back a message to the sender
        @:param message The message
        """
        self.clients[self.client].sendMessage(message, False)

    def sendToALl(self, message):
        """Send a message to all the clients
        @:param message The message
        """
        for user in self.clients:
            user.sendMessage(message, False)

    def handleMessage(self, message_in):
        """Send back a message to the sender
        @:param message_in The incoming message from the peer
        """
        parsed = json.loads(message_in)
        to = parsed.get('to', 'default')
        message = str(parsed.get('message', 'default'))
        all_clients = parsed.get('all', False)

        if all_clients:
            # All clients?
            self.sendToALl(message)
        else:
            # Send to the user a message "to is who"
            if to in self.clients:
                if to != self.client:
                    self.clients[to].sendMessage(message, False)
                    print "Message sent to " + to

        print "No action done"


# Run the server
def runServer(clients, port, timeout=5000):
    factory = WebSocketServerFactory("ws://localhost:" + str(port), debug=False)
    factory.protocol = WebSocket(clients)
    factory.setProtocolOptions(closeHandshakeTimeout=timeout)
    factory.isServer = True

    # Reactor TCP -> Interact with the protocol
    reactor.listenTCP(port, factory)
    reactor.run()


clients = {}
port = 9000

websocket_server = Process(target=runServer, args=(clients, port,))
# websocket_server.daemon = True
websocket_server.start()
