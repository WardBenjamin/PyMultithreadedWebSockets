from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import queue


class ServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open")

        def send_outbound():
            outbox = self.factory.game_outbox.to_list()
            for i in range(0, len(outbox)):
                self.sendMessage("{0}".format(outbox[i]).encode("utf8"))
            self.factory.game_outbox.clear()
            self.factory.reactor.callLater(self.factory.tick_delay, send_outbound)

        send_outbound()

    def onMessage(self, payload, isBinary):
        self.factory.game_inbox.put(payload)


class ServerFactory(WebSocketServerFactory):
    protocol = ServerProtocol

    def __init__(self, ws_uri, game_inbox, game_outbox, tick_delay):
        WebSocketServerFactory.__init__(self, ws_uri)
        self.game_inbox = game_inbox
        self.game_outbox = game_outbox
        self.tick_delay = tick_delay
