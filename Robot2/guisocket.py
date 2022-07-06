import socket
from protocol_client import Protocol
from threading import Thread
from PIL import Image, ImageTk
import PIL
from tkinter import DISABLED, NORMAL
import cv2
import os
from tkinter import *

class Socket:
    host='192.168.0.20'
    # host = '127.0.0.1'
    def __init__(self):
        self.on_message = {
            'frame': self.onFrameAsync,
            'bw_frame':self.onbwFrameAsync,
            'front_frame':self.onFrontFrameAsync,
            'signalData':self.onsignalData,
            "feedData":self.onfeedData,
            'u_there': lambda x: None

        }
        self.gui = None

    def connection(self):
        self.__protocol = Protocol(on_message_handlers=self.on_message, ip=self.host)
        self.gui.Connect_button.config(state=DISABLED)
        self.gui.Connect_button["text"] = "Connected"
        
    def quit(self):
        
        self.gui.Connect_button.config(state=NORMAL)
        self.gui.Connect_button["text"] = "Connect"
    
    def disconnect(self):
        self.__protocol.send_message('command', 'disconnect')

    def set_gui(self, gui):
        self.gui = gui

    def onFrameAsync(self, frame):
        Thread(target=self.onFrame, args=(frame,)).start()

    def onbwFrameAsync(self, bw_frame):
        Thread(target=self.onbwFrame, args=(bw_frame,)).start()


    
    def onFrontFrameAsync(self, front_frame):
        Thread(target=self.onFrontFrame, args=(front_frame,)).start()
    
    def onsignalData(self, signalData):
        Thread(target=self.onSignal, args=(signalData,)).start()
    def onfeedData(self, feedData):
        Thread(target=self.onfeed, args=(feedData,)).start()
    

    def onSignal(self,signalData):
        self.gui.plot.clear()
        self.gui.plt.clear()
        self.x = signalData.get("X")
        self.y = signalData.get("y")
        self.y1 = signalData.get("y1")
        #print(self.y)
        #print(self.y1)
        
        self.gui.plot.plot(self.x, self.y,color='red')
        self.gui.plt.plot(self.x, self.y1,color='blue')
        self.gui.canvas.draw()
        self.gui.plot.clear()
        self.gui.plt.clear()
        self.gui.Start_button.config(state=NORMAL)
    def onfeed(self,feedData):
        print(feedData)
        self.gui.Start_button.config(state=NORMAL)
        self.gui.Send_button.config(state=NORMAL)
        self.gui.Excel_button.config(state=NORMAL)
        self.gui.Right_button.config(state=NORMAL)
        self.gui.Forward_button.config(state=NORMAL)
        self.gui.Left_button.config(state=NORMAL)
        self.gui.Back_button.config(state=NORMAL)
        self.gui.A_button.config(state=NORMAL)
        self.gui.speed_Send_button.config(state=NORMAL)
        self.gui.position_Zero_button.config(state=NORMAL)
        
        self.gui.Original_button.config(state=NORMAL)
        self.gui.Off_button.config(state=NORMAL)
        print("All Done")
        
        
        
        

    def save(self):
        import pandas as pd
        from datetime import datetime
        import time
        today = datetime.now()

        directory = today.strftime('%Y%m%d')
       
        path = "Record"
        folder=os.path.join(path, directory)
        if not os.path.exists(folder):
            os.makedirs(folder)
        list_dict1 = {'X': self.x, 'y': self.y}
        list_dict2 = {'X': self.x, 'y': self.y1}
        
        df1 = pd.DataFrame(list_dict1)
        df2 = pd.DataFrame(list_dict2)
        time=time.time()
        file1="Channel1__"+ str(time)
        file2="Channel2__"+ str(time)
        filename1 = "%s.csv" % file1
        filename2 = "%s.csv" % file2
        

        df1.to_csv(folder + "/" + filename1, index=False)
        df2.to_csv(folder+ "/" + filename2, index=False)
        
        



    def onFrontFrame(self, front_frame):
        #global flag
        #flag = True

        
    
        frame = cv2.flip(front_frame, -1)
        frame = cv2.flip(frame, -1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        img = img.resize((600, 430))
        imgtk1 = ImageTk.PhotoImage(image=img)
        # label = Label(self.gui.Video2, image=imgtk)
        # label.place(x=10,y=50)
        self.gui.lmain2.imgtk = imgtk1

        self.gui.lmain2.configure(image=imgtk1)
        self.gui.lmain2.place(x=5, y=25)
        
        

        self.gui.top.update()






    def onFrame(self, frame):
        #global flag
        #flag = True

        
        frame = cv2.flip(frame, -1)
        frame = cv2.flip(frame, -1)
        frame2 = cv2.resize(frame, (512,512))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = PIL.Image.fromarray(cv2image)
        img = img.resize((300, 250))
        imgtk = ImageTk.PhotoImage(image=img)
        # label = Label(self.gui.Video2, image=imgtk)
        # label.place(x=10,y=50)
        self.gui.lmain.imgtk = imgtk

        self.gui.lmain.configure(image=imgtk)
        self.gui.lmain.place(x=5, y=15)
        import pandas as pd
        from datetime import datetime
        import time
        path1 = "Image"
        
        today = datetime.now()
        
       
        directory1 = today.strftime('%Y%m%d')
       
        folder1 = os.path.join(path1,directory1)
        if not os.path.exists(folder1):
            os.makedirs(folder1)
        time = time.time()
        file = str(time)
       
        cv2.imwrite(folder1 +'/' + str(file) + '.jpg', frame2)
        
        
        
        

        self.gui.top.update()

    def onbwFrame(self, bw_frame):
        # global flag
        # flag = True

        bw_frame = cv2.flip(bw_frame, 1)
        bw_frame = cv2.flip(bw_frame, 1)
        bw_frame2 = cv2.resize(bw_frame, (512,512))
        cv2image = cv2.cvtColor(bw_frame, cv2.COLOR_BGR2RGBA)
        #img = PIL.Image.fromarray(cv2image)
        img = cv2image.resize((300, 250))

        #imgtk = ImageTk.PhotoImage(image=img)
        # label = Label(self.gui.Video2, image=imgtk)
        # label.place(x=10,y=50)
        #self.gui.lmain.imgtk = imgtk

        #self.gui.lmain.configure(image=imgtk)
        #self.gui.lmain.place(x=5, y=15)
        import pandas as pd
        from datetime import datetime
        import time
        path1 = "BW"

        today = datetime.now()

        directory1 = today.strftime('%Y%m%d')

        folder1 = os.path.join(path1, directory1)
        if not os.path.exists(folder1):
            os.makedirs(folder1)
        time = time.time()
        file = str(time)

        cv2.imwrite(folder1 + '/' + str(file) + '.jpg', bw_frame2)

        self.gui.top.update()
    def video(self):
        self.gui.Original_button.config(state=DISABLED)
        self.__protocol.send_message('command', 'start_video')
        self.__protocol.send_message('command', 'start_bw_video')

        
    
    def front_video(self):
        self.gui.front_button.config(state=DISABLED)
        self.__protocol.send_message('command', 'start_front_video')
        
    def zero(self):
        
        self.__protocol.send_message('command', 'zero')
    
    
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
    
    def semiAuto(self):
        self.gui.Start_button.config(state=DISABLED)
        self.gui.Send_button.config(state=DISABLED)
        self.gui.Excel_button.config(state=DISABLED)
        self.gui.Right_button.config(state=DISABLED)
        self.gui.Forward_button.config(state=DISABLED)
        self.gui.Left_button.config(state=DISABLED)
        self.gui.Back_button.config(state=DISABLED)
        self.gui.A_button.config(state=DISABLED)
        self.gui.speed_Send_button.config(state=DISABLED)
        self.gui.position_Zero_button.config(state=DISABLED)
        
        self.gui.Original_button.config(state=DISABLED)
        self.gui.Off_button.config(state=DISABLED)
        self.__protocol.send_message("command", "semiAuto")

        #self.gui.Start_button.config(state=DISABLED)

    def trigger (self):
        time = self.gui.time_entry.get()
        trigger = self.gui.trig_entry.get()


        triggerData = {"time": time, "trigger": trigger}
        self.__protocol.send_message('triggerData', triggerData)

    def grid (self):
        G_X = self.gui.GX_entry.get()
        G_Y = self.gui.GY_entry.get()



        gridData = {"G_X": G_X, "G_Y": G_Y}
        self.__protocol.send_message('gridData', gridData)

    def speed (self):
        speed=self.gui.speed_entry.get()
        speedData = {"speed": speed}
        self.__protocol.send_message('speedData', speedData)

    def Quit(self):
        Quit_button = self.gui.Button(self.gui.top, text="Quit", fg="blue", command=quit).place(x=200, y=100)

    def release(self):
        self.__protocol.send_message('command', 'end_video')
        self.gui.Original_button.config(state=NORMAL)
    def front_release(self):
        self.__protocol.send_message('command', 'end_front_video')
        self.gui.front_button.config(state=NORMAL)

