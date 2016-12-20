# PyMultithreadedWebSockets

Implements a two-thread system, one that can run arbitrary code and one running a Twisted websocket server. These threads have bidirectional communication using two FIFO Queues

To run, run main.py, open the (FireFox or Chrome) developer console, create a WebSocket, and connect to 127.0.0.1:8001. You can send and recieve messages in both directions, though only through code in the python side.

Note: the websocket will broadcast all backlogged messages in the outbound queue the first time that a client connects.
