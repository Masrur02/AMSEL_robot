from tkinter import *
from matplotlib.figure import Figure
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
import PIL
import cv2
from multiprocessing import Process
import sys
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import socket
import cv2, pickle, struct
import time
from threading import *



class Gui:
    def __init__(self, net_connection):
        top = Tk()
        self.top = top
        self.top.title("ASMEL Robot Remote")
        self.top.geometry("1500x520")
        self.top.resizable(width=0,height=0)
        
        self.net_connection = net_connection

        # pass
        #Thread.__init__(self)
        self.Master = Frame(top, height=500,width=1480, highlightbackground='blue', highlightthickness=3)
        self.Master.place(x=5,y=5)
       
        self.Robot = Frame(self.Master, height=150,width=350, highlightbackground='blue', highlightthickness=3)
        self.Robot.place(x=160,y=33)
        self.Video = Frame(self.Master, height=150,width=80, highlightbackground='blue', highlightthickness=3)
        self.Video.place(x=680,y=33)
        self.Video2 = Frame(self.Master, height=293,width=330, highlightbackground='blue', highlightthickness=2)
        self.Video2.place(x=450,y=192)
        self.lmain = Label(self.Video2)
        self.Video2_label = Label(self.Video2, text="Video",fg='blue',font="Times 18").place(x=120, y=5)
        
        self.Video3 = Frame(self.Master, height=450,width=500, highlightbackground='blue', highlightthickness=2)
        self.Video3.place(x=950,y=30)
        self.lmain2 = Label(self.Video3)
        self.Video3_label = Label(self.Video3, text="Front Camera",fg='blue',font="Times 18").place(x=150, y=5)
        
        
        self.Network = Frame(top, height=150,width=150, highlightbackground='blue', highlightthickness=3)
        self.Network.place(x=15,y=40)
        self.Sensor = Frame(top, height=150,width=160, highlightbackground='blue', highlightthickness=3)
        self.Sensor.place(x=780,y=40)

        self.Grid = Frame(top, height=150,width=150, highlightbackground='blue', highlightthickness=3)
        self.Grid.place(x=530,y=40)

        self.Excel = Frame(self.Robot,height=120,width=140, highlightbackground='blue', highlightthickness=3)
        self.Excel.place(x=10,y=3)

        self.Navigation = Frame(self.Robot,  height=120,width=165, highlightbackground='blue', highlightthickness=3)
        self.Navigation.place(x=160,y=3)
        self.Network_label = Label(self.Master, text="Network Settings",font = "Times 16",fg="blue").place(x=5, y=3)
        
        self.Ip_label = Label(self.Network, text="IP",fg='blue',font="Times 10").place(x=10, y=40)
        name=StringVar()
        name.set("192.168.0.20")
        self.Ip_entry = Entry(self.Network,textvariable=name).place(x=30, y=40, width=100)
        
        self.Port_label = Label(self.Network, text="Port",fg='blue',font="Times 10").place(x=10, y=70)
        
        name2=StringVar()
        name2.set("58011")
        self.Port_entry = Entry(self.Network,textvariable=name2).place(x=40, y=70, width=90)
        self.Connect_button = Button(self.Network, text="Connect", fg="blue", command=self.net_connection.connection)
        self.Connect_button.place(x=20, y=100)
        #self.Quit_button = Button(self.Network, text="Quit", fg="blue", command=self.net_connection.quit)
        #self.Quit_button.place(x=100, y=100)

        #####Sensor_Box####
        self.Sensor_label = Label(self.Master, text="Sensor",font = "Times 16",fg="blue").place(x=830, y=3)
        self.Image_label = Label(self.Master, text="Detect",font = "Times 16",fg="blue").place(x=680, y=3)
        self.Robot_label = Label(self.Master, text="Robot",font = "Times 16",fg="blue").place(x=300, y=3)
        self.Grid_label = Label(self.Master, text="Grid",font = "Times 16",fg="blue").place(x=565, y=3)
        self.Start_button = Button(self.Sensor, text="Start", fg="blue",command=self.net_connection.signal)
        self.Start_button.place(x=55, y=110)
        self.time_label = Label(self.Sensor, text="time(ms)",fg='blue',font="Times 10").place(x=5, y=28)
        self.time_entry = Entry(self.Sensor)
        self.time_entry.place(x=58, y=30, width=90)
        self.trig_label = Label(self.Sensor, text="Trig(mv)",fg='blue',font="Times 10").place(x=5, y=50)
        self.trig_entry = Entry(self.Sensor)
        self.trig_entry.place(x=58, y=50, width=90)
        self.Send_button = Button(self.Sensor, text="Send", fg="blue", command=self.net_connection.trigger)
        self.Send_button.place(x=55, y=80)
        self.Excel_button = Button(self.Sensor, text="Save", fg="blue",command=self.net_connection.save)
        self.Excel_button.place(x=100, y=90)

        #####Grid_Box####
        self.GX_label = Label(self.Grid, text="G_x(m)",fg='blue',font="Times 10").place(x=5, y=28)
        self.GX_entry = Entry(self.Grid)
        self.GX_entry.place(x=58, y=30, width=70)
        
        self.GY_label = Label(self.Grid, text="G_y(m)",fg='blue',font="Times 10").place(x=5, y=58)
        self.GY_entry = Entry(self.Grid)
        self.GY_entry.place(x=58, y=58, width=70)

        self.SendGrid_button = Button(self.Grid, text="SendGrid", fg="blue", command=self.net_connection.grid)
        self.SendGrid_button.place(x=55, y=85)
    
        '''self.GY_label = Label(self.Grid, text="G_y(m)",fg='blue',font="Times 10").place(x=5, y=50)
        self.GY_entry = Entry(self.Grid)
        self.GY_entry.place(x=58, y=50, width=90)'''

        ######Excel_Box####
        self.Excel_label = Label(self.Excel, text="Robot Speed",font = "Times 12",fg="blue").place(x=25, y=3)
        
        self.speed_label = Label(self.Excel, text="Speed",fg='blue',font="Times 10").place(x=3, y=28)
        self.speed_entry = Entry(self.Excel)
        self.speed_entry.place(x=40, y=30, width=80)
        self.speed_Send_button = Button(self.Excel, text="Speed_Send", fg="blue", command=self.net_connection.speed)
        self.speed_Send_button.place(x=30, y=55)
        
        self.position_Zero_button = Button(self.Excel, text="position_Zero", fg="blue", command=self.net_connection.zero)
        self.position_Zero_button.place(x=30, y=85)
        #####Navigation_Box####
        self.Navigation_label = Label(self.Navigation, text="Robot Navigation",font = "Times 12",fg="blue").place(x=25, y=3)
        self.Forward_button = Button(self.Navigation, text="F", fg="blue")
        self.Forward_button.place(x=55, y=25)
        self.Forward_button.bind("<ButtonPress>", self.net_connection.F_on_press)
        self.Forward_button.bind("<ButtonRelease>", self.net_connection.F_on_release)

        self.Left_button = Button(self.Navigation, text="L", fg="blue")
        self.Left_button.place(x=25, y=50)
        self.Left_button.bind("<ButtonPress>", self.net_connection.L_on_press)
        self.Left_button.bind("<ButtonRelease>", self.net_connection.L_on_release)

        self.Right_button = Button(self.Navigation, text="R", fg="blue")
        self.Right_button.place(x=80, y=50)
        self.Right_button.bind("<ButtonPress>", self.net_connection.R_on_press)
        self.Right_button.bind("<ButtonRelease>", self.net_connection.R_on_release)
        self.Back_button = Button(self.Navigation, text="B", fg="blue")
        self.Back_button.place(x=55, y=80)
        self.Back_button.bind("<ButtonPress>", self.net_connection.B_on_press)
        self.Back_button.bind("<ButtonRelease>", self.net_connection.B_on_release)
        self.A_button = Button(self.Navigation, text="S.Auto", fg="blue",command=self.net_connection.semiAuto)
        self.A_button.place(x=110, y=50)


        self.fig = Figure(figsize=(6, 4))
        #self.fig.clf()
        a = self.fig.add_subplot(2,1,1)
        
        a.plot("", color='red')
        a.clear()
        b = self.fig.add_subplot(2,1,2)
        b.plot("", color='blue')
        b.clear()
       
        a.set_title("Elastic Waves", fontsize=25,color='b',fontname='Times New Roman')
        a.set_ylabel("Value", fontsize=14,color='b',fontname='Times New Roman')
        a.set_ylabel("Value", fontsize=14,color='b',fontname='Times New Roman')
        b.set_ylabel("Value", fontsize=14,color='b',fontname='Times New Roman')
        b.set_xlabel("Count", fontsize=14,color='b',fontname='Times New Roman')
        a.spines['bottom'].set_color('blue')
        a.spines['top'].set_color('blue')
        a.spines['right'].set_color('blue')
        a.spines['left'].set_color('blue')
        b.spines['bottom'].set_color('blue')
        b.spines['top'].set_color('blue')
        b.spines['right'].set_color('blue')
        b.spines['left'].set_color('blue')
        a.tick_params(axis='x', colors='blue')
        a.tick_params(axis='y', colors='blue')
        b.tick_params(axis='x', colors='blue')
        b.tick_params(axis='y', colors='blue')
        self.plot = a
        self.plt = b
        
        
        
       
        
        canvas = FigureCanvasTkAgg(self.fig, master=self.Master)
        canvas.get_tk_widget().pack(padx=1, pady=1)
        canvas.get_tk_widget().place(x=8,y=192,height=293,width=430)
        canvas.get_tk_widget().config(highlightbackground = "blue", highlightcolor= "blue",highlightthickness=2)
        canvas.draw()
        
        self.canvas = canvas
        
        
        
        
        
        ##### Original Video Streaming####
        #photo = PhotoImage(file="")

        #self.Original = Label(top, image=photo)
        self.Original_button = Button(self.Video, text="Video", fg="blue",command=self.net_connection.video)
        self.Original_button.place(x=10, y=20)
        self.Off_button = Button(self.Video, text="Video off", fg="blue", command=self.net_connection.release)
        self.Off_button.place(x=5, y=60)
        
        
        ####### Front Camera ########
        self.front_button = Button(self.Video3, text="Video", fg="blue",command=self.net_connection.front_video)
        self.front_button.place(x=90, y=10)
        self.front_Off_button = Button(self.Video3, text="Video off", fg="blue", command=self.net_connection.front_release)
        self.front_Off_button.place(x=300, y=10)

        self.Quit_button = Button(self.Network, text="Quit", fg="blue", command=sys.exit).place(x=100, y=100)

    def quit_safely(self):
        self.net_connection.disconnect()
        self.top.destroy()
