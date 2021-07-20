import socket
from protocol_client import Protocol
from threading import Thread
from PIL import Image, ImageTk
import PIL
from tkinter import DISABLED, NORMAL
import cv2
import os

class Socket:
    host='168.115.106.126'
    # host = '127.0.0.1'
    def __init__(self):
        self.on_message = {
            'frame': self.onFrameAsync,
            'signalData':self.onsignalData

        }
        self.gui = None

    def connection(self):
        self.__protocol = Protocol(on_message_handlers=self.on_message, ip=self.host)
        self.gui.Connect_button.config(state=DISABLED)
        self.gui.Connect_button["text"] = "Connected"
    
    def set_gui(self, gui):
        self.gui = gui

    def onFrameAsync(self, frame):
        Thread(target=self.onFrame, args=(frame,)).start()
    def onsignalData(self, signalData):
        Thread(target=self.onSignal, args=(signalData,)).start()

    def onSignal(self,signalData):

        self.x = signalData.get("X")
        self.y = signalData.get("Y")
        self.gui.plot.plot(self.x, self.y,color='red')
        self.gui.canvas.draw()
        self.gui.Start_button.config(state=NORMAL)

    def save(self):
        import pandas as pd
        from datetime import datetime
        import time
        today = datetime.now()

        directory = today.strftime('%Y%m%d')
        path = "E:/Work/Khan_robot/Record/"
        folder=os.path.join(path, directory)
        if not os.path.exists(folder):
            os.makedirs(folder)
        list_dict = {'X': self.x, 'Y': self.y}
        df = pd.DataFrame(list_dict)
        time=time.time()
        file=str(time)

        filename = "%s.csv" % file
        os.chdir(folder)

        df.to_csv(filename, index=False)



    def onFrame(self, frame):
        global flag
        flag = True


        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.gui.lmain.imgtk = imgtk

        self.gui.lmain.configure(image=imgtk)
        self.gui.lmain.grid(row=1, column=2)
        self.gui.top.update()

    def video(self):
        self.gui.Original_button.config(state=DISABLED)
        self.__protocol.send_message('command', 'start_video')
    def F_on_press(self,event):

        self.__protocol.send_message('button', 'F_on')
    def L_on_press(self,event):
        self.__protocol.send_message('button', 'L_on')
    def R_on_press(self,event):
        self.__protocol.send_message('button', 'R_on')
    def B_on_press(self,event):
        self.__protocol.send_message('button', 'B_on')
    def F_on_release(self,event):
        self.__protocol.send_message('button', 'F_off')
    def L_on_release(self,event):
        self.__protocol.send_message('button', 'L_off')
    def R_on_release(self,event):
        self.__protocol.send_message('button', 'R_off')
    def B_on_release(self,event):
        self.__protocol.send_message('button', 'B_off')


    def signal(self):
        self.gui.plot.clear()
        self.__protocol.send_message("command", "startSignal")

        self.gui.Start_button.config(state=DISABLED)

    def trigger (self):
        time = self.gui.time_entry.get()
        trigger = self.gui.trig_entry.get()


        triggerData = {"time": time, "trigger": trigger}
        self.__protocol.send_message('triggerData', triggerData)
    def speed (self):
        speed=self.gui.speed_entry.get()
        speedData = {"speed": speed}
        self.__protocol.send_message('speedData', speedData)

    def speed (self):
        speed=self.gui.speed_entry.get()
        speedData = {"speed": speed}
        self.__protocol.send_message('speedData', speedData)

    def Quit(self):
        Quit_button = self.gui.Button(self.gui.top, text="Quit", fg="blue", command=quit).place(x=1200, y=220)

    def release(self):
        self.__protocol.send_message('command', 'end_video')
        self.gui.Original_button.config(state=NORMAL)

