from tkinter import *
from matplotlib.figure import Figure
from PIL import Image,ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
import PIL
import cv2
from multiprocessing import Process

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
        self.top.title("AET Robot Remote")
        self.top.geometry("800x400")
        self.lmain = Label(self.top)
        self.net_connection = net_connection

        # pass
        #Thread.__init__(self)

        self.Network = Frame(top, width=100, highlightbackground='blue', highlightthickness=3)
        self.Network.grid(row=0, column=0, padx=50, pady=20, ipadx=20, ipady=70)
        self.Sensor = Frame(top, width=120, highlightbackground='blue', highlightthickness=3)
        self.Sensor.grid(row=0, column=1, padx=20, pady=20, ipadx=20, ipady=70)

        self.Excel = Frame(top, width=100, highlightbackground='blue', highlightthickness=3)
        self.Excel.grid(row=0, column=2, padx=20, pady=20, ipadx=20, ipady=70)

        self.Navigation = Frame(top, width=100, highlightbackground='blue', highlightthickness=3)
        self.Navigation.grid(row=0, column=3, padx=20, pady=20, ipadx=20, ipady=70)
        self.Network_label = Label(self.Network, text="Network Settings").place(x=25, y=5)
        self.Ip_label = Label(self.Network, text="IP").place(x=10, y=40)
        self.Ip_entry = Entry(self.Network).place(x=30, y=40, width=100)
        self.Port_label = Label(self.Network, text="Port").place(x=10, y=70)
        self.Port_entry = Entry(self.Network).place(x=40, y=70, width=90)
        self.Connect_button = Button(self.Network, text="Connect", fg="blue", command=self.net_connection.connection)
        self.Connect_button.place(x=40, y=100)

        #####Sensor_Box####
        self.Sensor_label = Label(self.Sensor, text="Sensor").place(x=50, y=5)
        self.Start_button = Button(self.Sensor, text="Start", fg="blue",command=self.net_connection.signal)
        self.Start_button.place(x=55, y=110)
        self.time_label = Label(self.Sensor, text="time(ms)").place(x=5, y=28)
        self.time_entry = Entry(self.Sensor)
        self.time_entry.place(x=58, y=30, width=90)
        self.trig_label = Label(self.Sensor, text="Trig(mv)").place(x=5, y=50)
        self.trig_entry = Entry(self.Sensor)
        self.trig_entry.place(x=58, y=50, width=90)
        self.Send_button = Button(self.Sensor, text="Send", fg="blue", command=self.net_connection.trigger)
        self.Send_button.place(x=55, y=80)

        ######Excel_Box####
        self.Excel_label = Label(self.Excel, text="Save and Speed").place(x=25, y=5)
        self.Excel_button = Button(self.Excel, text="Save", fg="blue",command=self.net_connection.save).place(x=40, y=90)
        self.speed_label = Label(self.Excel, text="Speed").place(x=3, y=28)
        self.speed_entry = Entry(self.Excel)
        self.speed_entry.place(x=40, y=30, width=80)
        self.speed_Send_button = Button(self.Excel, text="Speed_Send", fg="blue", command=self.net_connection.speed)
        self.speed_Send_button.place(x=30, y=60)
        #####Navigation_Box####
        self.Navigation_label = Label(self.Navigation, text="Navigation").place(x=40, y=5)
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
        self.A_button = Button(self.Navigation, text="Autonomous", fg="blue").place(x=30, y=110)


        self.fig = Figure(figsize=(6, 4))
        a = self.fig.add_subplot(111)
        a.plot("", color='red')
        a.clear()
        # a.invert_yaxis()

        a.set_title("Sensor Data", fontsize=16)
        a.set_ylabel("Value", fontsize=10)
        a.set_xlabel("Count", fontsize=10)
        self.plot = a
        canvas = FigureCanvasTkAgg(self.fig, master=top)
        canvas.get_tk_widget().grid(row=1, column=0)
        canvas.draw()
        self.canvas = canvas
        ##### Original Video Streaming####
        #photo = PhotoImage(file="")

        #self.Original = Label(top, image=photo)
        self.Original_button = Button(top, text="Video", fg="blue",command=self.net_connection.video)
        self.Original_button.place(x=1000, y=220)
        self.Off_button = Button(top, text="Video off", fg="blue", command=self.net_connection.release)
        self.Off_button.place(x=1100, y=220)

        self.Quit_button = Button(top, text="Quit", fg="blue", command=top.destroy).place(x=1200, y=220)

