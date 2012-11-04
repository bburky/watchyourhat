import socket
import threading
from collections import defaultdict
import time

pos = {}
allies = {}
ids = {}
s = None
msg_buff = []
msg_lock = threading.Lock()
hosting = False
my_id = 0

def init_network(connect_to=None):
    global s
    s = Socket(connect_to)

def receive_messages(r):
	while not s:
		time.sleep(.1)
	while True:
	    m = s.rcv(r)
	    
	    msg_lock.acquire()
	    msg_buff.append(m)
	    msg_lock.release()

def get_player_pos():
    return pos.values()

class Socket:
    def __init__(self, host=None):
        global hosting
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 12347
        self.rec = []
        self.msg = defaultdict(lambda: '')
        
        if host:
            print "I'm a client"
            self.sock.connect((host, port))
            self.rec.append(self.sock)
            threading.Thread(target=receive_messages, args=(self.sock,)).start()
        else:
            self.sock.bind(("0.0.0.0", port))
            self.sock.listen(99)
            threading.Thread(target=self.accept_all).start()
            hosting = True
            print "I'm a server"
    
    def accept_all(self):
        global ids
        n = 1
        while True:
            c, addr = self.sock.accept()
            
            s.send_one(c, '0 %d;' % n)
            self.rec.append(c)
            print "Someone connected"
            threading.Thread(target=receive_messages, args=(c,)).start()
            
            n += 1
    
    def send_one(self, tgt, msg):
        sent = 0
        while sent < len(msg):
            sent += tgt.send(msg[sent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")

        
    def send(self, msg):
        for r in self.rec:
            sent = 0
            while sent < len(msg):
                sent += r.send(msg[sent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
    
    def rcv(self, r):
        while True:
            chunk = r.recv(1)
            if chunk == '':
                raise RuntimeError("socket connection broken")
            
            self.msg[r] += chunk
            if ';' in self.msg[r]:
                msg = self.msg[r].split(';')[0]
                self.msg[r] = ';'.join(self.msg[r].split(';')[1:])
                return msg

