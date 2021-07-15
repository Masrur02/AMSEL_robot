import socket
from protocol import Protocol
import cv2
import pickle
from threading import Thread

class Server:
    def __init__(self):
        port = 5050
        host = socket.gethostbyname(socket.gethostname())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)

        self.__socket = s
        self.__is_connected = False
        self.__send_video = False
        self.__connection = None
        message_handlers = {
            'command': self.commandHandler,
            'button': self.onButtonClick
        }
        self.__protocol = Protocol(on_message_handlers=message_handlers)
    
    def commandHandler(self, command):
        commands = {
            'end_video': self.onEndVideo,
            'start_video': self.onStartVideo,
             "startSignal": self.onSignal,
             'autonomous': self.onAutonomous
        }
        commands.get(command)()
    def onButtonClick(self, button):
        buttons = {
            'F_on': self.F_on,
            'F_off': self.F_off,
            "L_on": self.L_on,
            'L_off': self.L_off,
            'R_on': self.R_on,
            'R_off': self.R_off,
            "B_on": self.B_on,
            'B_off': self.B_off,
        }
        buttons.get(button)()

    def __runRecvThread(self):
        Thread(target=self.__protocol.recv_message).start()

    def waitForConnetion(self):
        print('Waiting for connection...')
        conn, add = self.__socket.accept()
        self.__connection = conn
        self.__protocol.setSocketConnection(self.__connection)
        self.__is_connected = True
        self.__runRecvThread()
        print(f"Connection from {add} has been established.")
    
    @property
    def isConnected(self):
        return self.__is_connected
    
    def onStartVideo(self):
        thread = Thread(target=self.start_video_stream)
        thread.start()
    def onSignal(self):
        thread = Thread(target=self.startSignal)
        thread.start()

    def onAutonomous(self):
        thread = Thread(target=self.autonomous)
        thread.start()

    def F_on(self):
        thread = Thread(target=self.forward)
        thread.start()

    def F_off(self):
        thread = Thread(target=self.stop)
        thread.start()

    def L_on(self):
        thread = Thread(target=self.left)
        thread.start()

    def L_off(self):
        thread = Thread(target=self.stop)
        thread.start()

    def R_on(self):
        thread = Thread(target=self.right)
        thread.start()

    def R_off(self):
        thread = Thread(target=self.stop)
        thread.start()

    def B_on(self):
        thread = Thread(target=self.back)
        thread.start()

    def B_off(self):
        thread = Thread(target=self.stop)
        thread.start()

    def onEndVideo(self):
        self.__send_video = False


    def startSignal(self):
        X=[1,2,3]


        Y=[]
        for i in range(len(X)):
            y=X[i]*10
            Y.append(y)
        signalData={"X":X,"Y":Y}
        self.__protocol.send_message('signalData', signalData)







    def start_video_stream(self):
        if self.__send_video:
            return # ignore if already sending videos
        self.__send_video = True
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            _, frame = vid.read()
            self.__protocol.send_message('frame', frame)
            if not self.__send_video:
                vid.release()

    def forward(self):
        print("Forward")
    def left(self):
        print("Left")
    def right(self):
        print("Right")
    def back(self):
        print("Back")
    def stop(self):
        print("Stop")



if __name__ == "__main__":
    server = Server()
    server.waitForConnetion()

