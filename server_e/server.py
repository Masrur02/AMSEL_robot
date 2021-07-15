from enum import Flag
import socket
from protocol import Protocol
import cv2
import pickle
from threading import Thread
import RPi.GPIO as GPIO
import time
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

ads = ADS.ADS1115(i2c)


class Server:
    def __init__(self):
        port = 5050
        host ="168.115.106.126"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)
        self.LB = 21 # BOARD pin 12
        self.LF = 22  # BOARD pin 16
        self.RF=7   # BOARD pin 19
        self.RB=31   # BOARD pin 24
        GPIO.setwarnings(False) 
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(self.LB, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LF, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.RF, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.RB, GPIO.OUT, initial=GPIO.LOW)
        
            
            


       
        
        
        
        self.__socket = s
        self.__is_connected = False
        self.__send_video = False
        self.__connection = None
        message_handlers = {
            'command': self.commandHandler,
            'button': self.onButtonClick,
            'triggerData': self.onTriggerData
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
    '''def read(self):
        while True:
            self.a = AnalogIn(ads, ADS.P0)
            self.b=self.a.voltage*1000
            #print(self.b)
            #time.sleep(0.5)'''
    
        
        
    
    @property
    def isConnected(self):
        return self.__is_connected
    
    def onStartVideo(self):
        thread = Thread(target=self.start_video_stream)
        thread.start()
    def onSignal(self):
        thread = Thread(target=self.startSignal)
        thread.start()
    def onTriggerData(self, triggerData):
        Thread(target=self.onTrigger, args=(triggerData,)).start()

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

    def onTrigger(self,triggerData):
        self.time = triggerData.get("time")
        self.trigger = triggerData.get("trigger")
    def startSignal(self):
        
        
        while True:
            t=int(self.time)
            t_end = time.time() + t/1000
            trigger=int(self.trigger)
            Y=[]
            val = AnalogIn(ads, ADS.P0)
            
            val=val.value
            print("val",val)
            if val>=trigger:
                break
        for i in range(100):
            #print("Khan")
            val = AnalogIn(ads, ADS.P0)
            
            reading=val.value
            print("reading",reading)
            Y.append(reading)
        s=(len(Y))
        X=list(range(s))
        print(s)
        print(X)
        print(Y)
        signalData={"X":X,"Y":Y}
        self.__protocol.send_message('signalData', signalData)
                
            








    def start_video_stream(self):
        if self.__send_video:
            return # ignore if already sending videos
        self.__send_video = True
       
        vid = cv2.VideoCapture("/dev/video0")
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        vid.set(cv2.CAP_PROP_FPS, 25)
        
        while(vid.isOpened()):
            _, frame = vid.read()
            self.__protocol.send_message('frame', frame)
            if not self.__send_video:
                vid.release()

    def forward(self):
        print("Forward")
        
        GPIO.output(self.LF, GPIO.HIGH)
        GPIO.output(self.RF, GPIO.HIGH)
        GPIO.output(self.LB, GPIO.LOW)
        GPIO.output(self.RB, GPIO.LOW)
    def left(self):
        print("Left")
        GPIO.output(self.RF, GPIO.HIGH)
        GPIO.output(self.RB, GPIO.LOW)
        GPIO.output(self.LF, GPIO.LOW)
        GPIO.output(self.LB, GPIO.HIGH)
         
    def right(self):
        print("Right")
        GPIO.output(self.RF, GPIO.LOW)
        GPIO.output(self.RB, GPIO.HIGH)
        GPIO.output(self.LF, GPIO.HIGH)
        GPIO.output(self.LB, GPIO.LOW)
    def back(self):
        print("Back")
        GPIO.output(self.LB, GPIO.HIGH)
        GPIO.output(self.LF, GPIO.LOW)
        GPIO.output(self.RF, GPIO.LOW)
        GPIO.output(self.RB, GPIO.HIGH)
        
    def stop(self):
        print("Stop")
        GPIO.output(self.LB, GPIO.LOW)
        GPIO.output(self.LF, GPIO.LOW)
        GPIO.output(self.RF, GPIO.LOW)
        GPIO.output(self.RB, GPIO.LOW)

        
    


if __name__ == "__main__":
    server = Server()
    server.waitForConnetion()
    #server.read()
    
        
    
  

