import struct
import pickle
from hashlib import md5
from os import urandom
from threading import Thread
from socket import socket as stock_socket
from socket import TCP_NODELAY, IPPROTO_TCP, SHUT_RDWR
from queue import Queue
import time
import warnings

CHUNK_SIZE = 32 * 1024

warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

class Socket:
    def __init__(self, address='0.0.0.0', port=58011, mode='server', queue=False, nodelay=True):
        assert mode in ['server', 'client']
        self.is_queue = queue
        self.__is_connected = False
        self.__socket = stock_socket()
        self.__socket_type = mode
        self.__will_send_queue = True
        self.__disconnected = False

        if nodelay:
            self.__socket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        if mode == 'server':
            self.__socket.bind((address, port))
            self.__socket.listen(1)
        else:
            self.__socket.connect((address, port))
            self.__is_connected = True
            self.__connection = self.__socket

        if queue:
            self.__queue_size = 0
            self.__send_queue = Queue()
            thread = Thread(target=self.__keep_sending_queue)
            thread.isDaemon = True
            thread.start()

    def __keep_sending_queue(self):
        while self.__will_send_queue:
            if self.__queue_size > 0:
                self.__queue_size -= 1
                message_type, message_content = self.__send_queue.get_nowait()
                self.__send_message_impl(message_type, message_content)

    def diconnect(self):
        self.__disconnected = True
        self.__will_send_queue = False
        self.__is_connected = False
        #time.sleep(2) # finish current sending
        #self.__socket.shutdown(SHUT_RDWR)
        self.__socket.close()

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
        #print('sending...', message_id)
        #print('sending...', message_id)
        try:
            self.__connection.sendall(to_send)
        except:
            raise RuntimeError

    def send_message(self, message_type, message_content):
        if self.__disconnected:
            return
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
        if not self.__is_connected:
            return None, None
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
    def __init__(self, on_message_handlers, front_port=59010,bw_port=59085,video_port=59083, data_port=59084):
        assert int(video_port) != int(data_port) != int(front_port), 'Video and data port can not be the same.'
        self.__video_port = video_port
        self.__data_port = data_port
        self.__front_port = front_port
        self.__bw_port = bw_port
        self.__on_message_handlers = on_message_handlers
        self.__video_socket = None
        self.__data_socket = None
        self.__front_socket = None
        self.__bw_socket = None
        self.reinit()


    def reinit(self):
        self.__is_ready = False
        self.will_recv_data = False
        self.__pool_connection = False
        time.sleep(.1)

        try:
            if self.__video_socket:
                self.__video_socket.diconnect()
                print('Disconneted Video Socket.')
            if self.__data_socket:
                self.__data_socket.diconnect()
                print('Disconneted Data Socket.')
            if self.__front_socket:
                self.__front_socket.diconnect()
                print('Disconneted FrontSocket.')
            if self.__bw_socket:
                self.__bw_socket.diconnect()
                print('Disconneted bwSocket.')
        except:
            print('Disconnect Error.')
        
        self.__video_socket = Socket(port=self.__video_port)
        self.__data_socket = Socket(port=self.__data_port)
        self.__front_socket = Socket(port=self.__front_port)
        self.__bw_socket = Socket(port=self.__bw_port)
        
        print('Waiting for connection...')

        Thread(target=self.__video_socket.wait_for_connection).start()
        Thread(target=self.__data_socket.wait_for_connection).start()
        Thread(target=self.__front_socket.wait_for_connection).start()
        Thread(target=self.__bw_socket.wait_for_connection).start()
        Thread(target=self.__check_ready).start()

        check_connection_thread = Thread(target=self.__check_connected)
        check_connection_thread.daemon = True
        check_connection_thread.start()

    def __check_connected(self):
        while not self.__pool_connection:
            time.sleep(.5)
        while self.__pool_connection:
            try:
                self.__data_socket.send_message('u_there','hi')
                time.sleep(.5)
            except:
                self.reinit()

    def send_message(self, message_type, message_content):
        if message_type == 'frame':
            try:
                self.__video_socket.send_message(message_type, message_content)
            except ConnectionResetError:
                if self.__is_ready:
                    self.reinit()
        if message_type == 'front_frame':
            try:
                self.__front_socket.send_message(message_type, message_content)
            except ConnectionResetError:
                if self.__is_ready:
                    self.reinit()
        if message_type == 'bw_frame':
            try:
                self.__bw_socket.send_message(message_type, message_content)
            except ConnectionResetError:
                if self.__is_ready:
                    self.reinit()
        else:
            try:
                self.__data_socket.send_message(message_type, message_content)
            except ConnectionResetError:
                if self.__is_ready:
                    self.reinit()

    def send_frame(self, frame):
        self.__video_socket.send_message('frame', frame)
    def send_bw_frame(self, bw_frame):
        self.__bw_socket.send_message('bw_frame',bw_frame)
    def send_front_frame(self, front_frame):
        self.__front_socket.send_message('front_frame', front_frame)

    def __recv_execute_data(self):
        try:
            msg_type, msg_content = self.__data_socket.recv_a_message()
        except ConnectionResetError:
            if self.__is_ready:
                self.reinit()
            return
        if msg_type is None:
            return
        print(msg_type, '')
        Thread(target=self.__on_message_handlers.get(msg_type), args=(msg_content,)).start()

    def __check_ready(self):
        while True:
            if self.__video_socket.isConnected and self.__data_socket.isConnected and self.__bw_socket.isConnected and self.__front_socket.isConnected:
                self.__pool_connection = True
                self.__is_ready = True
                break
            time.sleep(1)

    @property
    def is_ready(self):
        return self.__is_ready

    def wait_untill_ready(self):
        while not self.__is_ready:
            time.sleep(1)

    def recv_data_forever(self):
        while True:
            if not self.__is_ready:
                time.sleep(.05)
            self.will_recv_data = True
            while self.will_recv_data:
                self.__recv_execute_data()
