import struct
import pickle
from hashlib import md5
from os import urandom

CHUNK_SIZE = 32 * 1024

class Protocol:
    def __init__(self, connection=None, on_message_handlers=None):
        self.socket = connection
        self.queue = []
        self.on_message = on_message_handlers
    
    def setSocketConnection(self, connection):
        self.socket = connection

    def send_message(self, message_type, message_content):
        message_content = pickle.dumps(message_content)
        message_id = md5(urandom(512)).hexdigest()
        headers = {
            'message_type': message_type,
            'message_id': message_id,
            'message_length': len(message_content)
        }
        headers = pickle.dumps(headers)
        to_send = struct.pack('Q', len(headers)) + headers + message_content
        print('sending...', message_id)
        self.queue.append(message_id)
        try:
            self.socket.sendall(to_send)
        except:
            self.queue.remove(message_id)
            raise RuntimeError
    
    def recv_fully(self, size):
        print('Recving...', size)
        msg_size = size
        data = b''
        while msg_size > 0:
            if msg_size > CHUNK_SIZE:
                packet = self.socket.recv(CHUNK_SIZE)
                data += packet
                msg_size -= len(packet)
            else:
                packet = self.socket.recv(msg_size)
                data += packet
                msg_size -= len(packet)
        return data

    def recv_message(self):
        while True:
            header_size = struct.unpack("Q", self.recv_fully(struct.calcsize('Q')))[0]
            headers = pickle.loads(self.recv_fully(header_size))
            message = pickle.loads(self.recv_fully(headers.get('message_length')))
            if headers.get('message_type') == 'ACK':
                self.queue.remove(message)
            else:
                self.send_message('ACK', headers.get('message_id'))
                self.on_message.get(headers.get('message_type'))(message)




