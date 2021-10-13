import struct
import pickle
from hashlib import md5
from os import urandom
from threading import Thread
from socket import socket as stock_socket
from socket import TCP_NODELAY, IPPROTO_TCP
from queue import Queue
import time

CHUNK_SIZE = 32 * 1024

class Socket:
    def __init__(self, address='0.0.0.0', port=58011, mode='server', queue=False, nodelay=True):
        assert mode in ['server', 'client']
        self.is_queue = queue
        self.__is_connected = False
        self.__socket = stock_socket()
        self.__socket_type = mode
        
        if nodelay:
            self.__socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        if mode == 'server':
            self.__socket.bind((address,port))
            self.__socket.listen(5)
        else:
            self.__socket.connect((address,port))
            self.__is_connected = True
            self.__connection = self.__socket
        
        if queue:
            self.__queue_size = 0
            self.__send_queue = Queue()
            thread = Thread(target=self.__keep_sending_queue)
            thread.isDaemon = True
            thread.start()

    def __keep_sending_queue(self):
        while True:
            if self.__queue_size > 0:
                self.__queue_size -= 1
                message_type, message_content = self.__send_queue.get_nowait()
                self.__send_message_impl(message_type, message_content)

    def __send_message_impl(self, message_type, message_content):
        message_content = pickle.dumps(message_content)
        message_id = md5(urandom(512)).hexdigest()
        headers = {
            'message_type': message_type,
            'message_id': message_id,
            'message_length': len(message_content)
        }
        headers = pickle.dumps(headers)
        to_send = struct.pack('!Q', len(headers)) + headers + message_content
        print('sending...', message_id)
        try:
            self.__connection.sendall(to_send)
        except:
            raise RuntimeError

    def send_message(self, message_type, message_content):
        if self.is_queue:
            self.__send_queue.put_nowait((message_type, message_content))
            self.__queue_size += 1
        else:
            self.__send_message_impl(message_type, message_content)

    def __recv_fully(self, size):
        msg_size = size
        data = b''
        while msg_size > 0:
            if msg_size > CHUNK_SIZE:
                packet = self.__connection.recv(CHUNK_SIZE)
                data += packet
                msg_size -= len(packet)
            else:
                packet = self.__connection.recv(msg_size)
                data += packet
                msg_size -= len(packet)
        return data

    def recv_a_message(self):
        header_size = struct.unpack("!Q", self.__recv_fully(struct.calcsize('!Q')))[0]
        headers = pickle.loads(self.__recv_fully(header_size))
        message = pickle.loads(self.__recv_fully(headers.get('message_length')))
        return headers.get('message_type'), message

    def wait_for_connection(self):
        if not self.__is_connected:
            connection, addr = self.__socket.accept()
            self.__connection = connection
            self.__is_connected = True
            print(f'Connection form {addr}')

    @property
    def isConnected(self):
        return self.__is_connected

class Protocol:
    def __init__(self, on_message_handlers, video_port=59083, data_port=59084, ip='127.0.0.1'):
        self.__video_socket = Socket(port=video_port, address=ip, mode='client')
        self.__data_socket = Socket(port=data_port, address=ip, mode='client')
        self.__on_message_handlers = on_message_handlers
        self.__is_ready = False

        data_thread = Thread(target=self.__recv_forever_data)
        data_thread.daemon = True
        self.__data_thread = data_thread

        video_thread = Thread(target=self.__recv_forever_video)
        video_thread.daemon = True
        self.__video_thread = video_thread
        
        Thread(target=self.__video_socket.wait_for_connection).start()
        Thread(target=self.__data_socket.wait_for_connection).start()
        Thread(target=self.__check_ready).start()
    
    def send_message(self, message_type, message_content):
        if message_type == 'frame':
            self.__video_socket.send_message(message_type, message_content)
        else:
            self.__data_socket.send_message(message_type, message_content)
    
    def send_frame(self, frame):
        self.__video_socket.send_message('frame', frame)

    def __recv_forever_data(self):
        while True:
            msg_type, msg_content = self.__data_socket.recv_a_message()
            Thread(target=self.__on_message_handlers.get(msg_type), args=(msg_content,)).start()

    def __recv_forever_video(self):
        while True:
            msg_type, msg_content = self.__video_socket.recv_a_message()
            Thread(target=self.__on_message_handlers.get(msg_type), args=(msg_content,)).start()

    def __check_ready(self):
        while True:
            if self.__video_socket.isConnected and self.__data_socket.isConnected:
                self.__is_ready = True
                self.__data_thread.start()
                self.__video_thread.start()
                break
            time.sleep(1)
    
    @property
    def is_ready(self):
        return self.__is_ready
    
    def wait_untill_ready(self):
        while not self.__is_ready:
            time.sleep(1)
