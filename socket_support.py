from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import queue


class ServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open")
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        self.factory.game_inbox.put(payload)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class ServerFactory(WebSocketServerFactory):
    protocol = ServerProtocol

    def __init__(self, ws_uri, game_inbox, game_outbox, tick_delay):
        WebSocketServerFactory.__init__(self, ws_uri)
        self.game_inbox = game_inbox
        self.game_outbox = game_outbox
        self.clients = []
        self.tick_delay = tick_delay
        self.tick_count = 0
        self.tick()

    def tick(self):
        self.tick_count += 1
        self.broadcast()
        self.reactor.callLater(self.tick_delay, self.tick)

    def register(self, client):
        if client not in self.clients:
            print("Registered new client {0}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("Unregistered client {0}".format(client.peer))

    def broadcast(self):
        """
        Requires use of an ImprovedQueue
        Note that this will broadcast all backlogged messages the first time that a client connects.
        """
        if len(self.clients) > 0:
            # print("Broadcasting queued messages")
            outbox = self.game_outbox.to_list()
            self.game_outbox.clear()
            for i in range(0, len(outbox)):
                prepared_msg = self.prepareMessage("{0}".format(outbox[i]).encode("utf8"))
                for c in self.clients:
                    c.sendPreparedMessage(prepared_msg)
