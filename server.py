import asynchat
import asyncore
import socket
from os import system
 
chat_room = {}
 
class ChatHandler(asynchat.async_chat):
    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock=sock, map=chat_room)
 
        self.set_terminator('\n')
        self.buffer = []
 
    def collect_incoming_data(self, data):
        self.buffer.append(data)
 
    def found_terminator(self):
        msg = ''.join(self.buffer)
        print msg
        for handler in chat_room.itervalues():
            if hasattr(handler, 'push'):
                handler.push(msg + '\n')
        self.buffer = []
 
class ChatServer(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('0.0.0.0', 5555))
        print "serving on port 5555"
        self.listen(5)
 
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = ChatHandler(sock)
 
server = ChatServer()
 
asyncore.loop(map=chat_room)
