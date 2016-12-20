from threading import Thread
import queue
from queue_hack import ImprovedQueue
import time


from socket_support import ServerProtocol, ServerFactory


def run_reactor(game_inbox, game_outbox):
    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = ServerFactory(u"ws://127.0.0.1:8001", game_inbox, game_outbox, 0.2)

    reactor.listenTCP(8001, factory)
    reactor.run(installSignalHandlers=0)


def run_game_logic(in_queue, out_queue):
    while True:
        while True:
            try:
                data = in_queue.get(block=False)
                print("Got payload: {}".format(data))
                in_queue.task_done()
            except queue.Empty:
                break;
        out_queue.put("Game message")
        time.sleep(1)

if __name__ == '__main__':
    game_inbox, game_outbox = ImprovedQueue(), ImprovedQueue()
    thread1 = Thread(target=run_game_logic, args=(game_inbox, game_outbox,))
    thread2 = Thread(target=run_reactor, args=(game_inbox, game_outbox,))

    thread1.start()
    thread2.start()
