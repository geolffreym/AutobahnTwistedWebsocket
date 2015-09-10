from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory, listenWS

import json


# The Protocol Handler WebSocket
class ServerProtocol(WebSocketServerProtocol):
    user = None

    def onOpen(self):
        print "Connection open"

    def onConnect(self, request):
        self.user = request.params.get('user')[0]
        self.factory.register(self)

        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            self.factory.handleMessage(payload, self)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


# The Factory
class ServerFactory(WebSocketServerFactory):
    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = {}

    def register(self, protocol):
        if protocol.user not in self.clients:
            print("Registered client {}".format(protocol.user))
            self.clients[protocol.user] = protocol

    def unregister(self, protocol):
        if protocol.user in self.clients:
            print("Unregistered client {}".format(protocol.user))
            del self.clients[protocol.user]

    def processMsg(self, msg):
        try:
            return json.loads(msg)
        except ValueError:
            return msg

    def handleMessage(self, msg, protocol):
        json = self.processMsg(msg)

        if 'to' in json:
            self.sendTo(json.get('to'), msg, protocol)
        else:
            if 'all' in json:
                self.sendAll(msg, protocol)

    def sendTo(self, usr, msg, protocol):
        if usr not in self.clients:
            context = dict()
            context['offline'] = True
            context['user'] = usr
            protocol.sendMessage(json.dumps(context))
            return

        if usr != protocol.user:
            print("Message sent to {}".format(usr))
            self.clients[usr].sendMessage(msg)

    def sendAll(self, msg, protocol):
        for k, c in self.clients.items():
            self.sendTo(k, msg, protocol)


if __name__ == '__main__':
    from twisted.internet import reactor

    port, debug = 8000, False
    factory = ServerFactory("ws://localhost:" + str(port),
                            debug=debug,
                            debugCodePaths=debug)

    factory.protocol = ServerProtocol
    factory.isServer = True
    factory.setProtocolOptions(
        allowHixie76=True,
        allowedOrigins=[]
    )

    listenWS(factory)
    reactor.run()
