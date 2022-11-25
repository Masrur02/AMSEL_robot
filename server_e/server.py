# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:46:47 2022

@author: almas
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:46:47 2022

@author: almas
"""
import imutils
from enum import Flag
import socket
from protocol_server import Protocol
import cv2
import pickle
from threading import Thread
import matplotlib.pyplot as plt
import time
import nidaqmx
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge, Slope
from nidaqmx.constants import AcquisitionType
import pandas as pd
import time
import time
from serial import Serial
import numpy as np
import cv2
from semi import Motor
from semi import MotorDriver
from semi import Video,eSignal

import tensorflow as tf
from tensorflow import keras
from tensorflow import keras
from tensorflow.keras.models import load_model
import tensorflow.keras.backend as K



# Load Keras model


class Server:
    def __init__(self):
        s3=Motor(port='COM3', baudrate=19200)
        s4=Motor(port='COM4', baudrate=19200, direction=-1)
        s5=Motor(port='COM5', baudrate=19200)
        s6=Motor(port='COM6', baudrate=19200,direction=-1)
        s7=Motor(port='COM7', baudrate=9600, write_timeout=0)
        s3.flush()
        s4.flush()
        s5.flush()
        s6.flush()
        
        self.s3=s3
        self.s4=s4
        self.s5=s5
        self.s6=s6
        self.s7=s7
        
        
        
        self.__send_video = False
        self.__send_front_video = False
        message_handlers = {
            'command': self.commandHandler,
            'button': self.onButtonClick,
            'triggerData': self.onTriggerData,
            'gridData': self.onGridData,
            'speedData': self.onSpeedData
        }
        self.__protocol = Protocol(on_message_handlers=message_handlers)

    def commandHandler(self, command):
        commands = {
            'frameDown':self.onFrameDown,
            'frameUp':self.onFrameUp,
            'sol':self.onSol,
            'lsol':self.onlSol,
            'rsol':self.onrSol,
            'end_video': self.onEndVideo,
            'start_video': self.onStartVideo,
            "start_front_video":self.onFrontVideo,
            "start_bw_video":self.onStartVideo,
            'end_front_video': self.offFrontVideo,
            "startSignal": self.onSignal,
            'semiAuto': self.onSemiAuto,
            'zero':self.zeroPos,
            'disconnect': self.disconnect
        }
        commands.get(command)()

    def disconnect(self):
        self.onEndVideo()
        self.__protocol.reinit()

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

    def serve_forever(self):
        print('Waiting for connection.')
        self.__protocol.wait_untill_ready()
        self.__protocol.recv_data_forever()

    def onSemiAuto(self):
        thread = Thread(target=self.SemiAuto)
        thread.start()

    def onSol(self):
        thread = Thread(target=self.Sol)
        thread.start()

    def onlSol(self):
        thread = Thread(target=self.lSol)
        thread.start()
        print("Khan")

    def onrSol(self):
        thread = Thread(target=self.rSol)
        thread.start()
        print("Tuli")

    
    def onFrameDown(self):
        thread = Thread(target=self.start_frame_down)
        thread.start()

    def onFrameUp(self):
        thread = Thread(target=self.start_frame_up)
        thread.start()

    def onFrontVideo(self):
        thread = Thread(target=self.start_front_stream)
        thread.start()
    
    def onAutonomous(self):
        thread = Thread(target=self.Auto)
        thread.start()   

    def onStartVideo(self):
        thread = Thread(target=self.start_video_stream)
        thread.start()

    def zeroPos(self):
        thread = Thread(target=self.zeroPosition)
        thread.start()

    def onSignal(self):
        thread = Thread(target=self.startSignal)
        thread.start()

    def onTriggerData(self, triggerData):
        Thread(target=self.onTrigger, args=(triggerData,)).start()

    def onGridData(self, gridData):
        Thread(target=self.onGrid, args=(gridData,)).start()

    def onSpeedData(self, speedData):
        Thread(target=self.onSpeed, args=(speedData,)).start()

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


    def start_frame_down(self):
        
        down = b'\x5A\xF1\x01\x00\x36\xB0\x00\x32'
        self.s7.write(down)
        self.s7.read(16)
        self.s7.write(down)
        self.s7.read(16)
        self.s7.write(down)
        self.s7.read(16)
        

    def start_frame_up(self):
        up=b'\x5A\xF1\x01\x01\x36\xB0\x00\x33'
        self.s7.write(up)
        self.s7.read(16)
        self.s7.write(up)
        self.s7.read(16)
        self.s7.write(up)
        self.s7.read(16)
        

    

    def Sol(self):

        sol1 = b'\x5A\xF1\x02\x01\x05\x0A\x00\x5D'
        sol2 = b'\x5A\xF1\x03\x01\x05\x0A\x00\x5E'
        self.s7.write(sol1)
        a=self.s7.read(16)
        self.s7.write(sol2)
        a=self.s7.read(16)
        
        
        
        #self.onlSol()
        #self.onrSol()
        



    def lSol(self):

        LSOL =b'\x5A\xF1\x02\x01\x05\x0A\x00\x5D'
        
        self.s7.write(LSOL)
        a=self.s7.read(16)
        

    def rSol(self):

        RSOL =  b'\x5A\xF1\x03\x01\x05\x0A\x00\x5E'
       
        
        self.s7.write(RSOL)
        a=self.s7.read(16)
        
        


        

         
         
        
         
         



    def zeroPosition(self):
        z=bytearray([183,184,1,13,1,10,120])
        regi=bytearray([183,184,1,130,2,5,0,7])
        self.s3.write(regi)
        self.s4.write(regi)
        self.s5.write(regi)
        self.s6.write(regi)
        self.s3.write(z)
        self.s4.write(z)
        self.s5.write(z)
        self.s6.write(z)
        self.switch=bytearray([183,184,1,5,1,1,137])
        self.s5.write(self.switch)
        
        

        

    def offFrontVideo(self):
        self.__send_front_video = False

    def onTrigger(self, triggerData):
        self.time = triggerData.get("time")
        self.trigger = triggerData.get("trigger")

    def onGrid(self, gridData):
        self.G_X = gridData.get("G_X")
        self.G_X=float(self.G_X)
        self.G_Y = gridData.get("G_Y")
        self.G_Y=float(self.G_Y)


    def onSpeed(self, speedData):
        self.speed = speedData.get("speed")
        #print(self.speed)
        self.speed=int(self.speed)
        
        self.posSpeed=self.speed%256
        self.posSpeed=int(self.posSpeed)
        print(self.posSpeed)
        
        self.negSpeed=256-self.posSpeed
        
        self.posStop=int(self.speed/256)
        print(self.posStop)
        self.negStop=int(255-self.posStop)

        Summation=500
        one=bin(1)
        self.posSum=int(500+self.posSpeed+self.posStop)
        self.negSum=int(500+self.negSpeed+self.negStop)
        #print(self.posSum)
        #print(self.negSum)
        self.posBin=bin(self.posSum)
        self.negBin=bin(self.negSum)
        self.posBin=self.posBin[-8:]
        self.negBin=self.negBin[-8:]

        def onescomplement(a):
            b=''
            for i in a:
            
                i=1-int(i)
                i=str(i)
           
                b+=i
            
            return b
        self.posCom=onescomplement(self.posBin)
        self.negCom=onescomplement(self.negBin)
            
        self.posChk=bin(int(self.posCom, 2) + int(one, 2))
        self.negChk=bin(int(self.negCom, 2) + int(one, 2))

        self.posChk=int(self.posChk,2)
        print(self.posChk)
        self.negChk=int(self.negChk,2)
        self.values35=bytearray([183,184,1,130,2,self.posSpeed,self.posStop,self.posChk])

        self.values46=bytearray([183,184,1,130,2,self.negSpeed,self.negStop,self.negChk])
        self.values=bytearray([183,184,1,130,2,0,0,12])
        
    def startSignal(self):

        
        t_ms = int(self.time)


        Triggering = float(self.trigger)
        t_s = .001 * t_ms
        #print(t_s)
        fre = 50000
        Num_samples = int(t_s * fre)

        N = 100000
        pre = 10
        pre_trig = int(10 / 100 * Num_samples)
        def istest():
            number = 1

            task = nidaqmx.Task()

            task.ai_channels.add_ai_accel_chan("cDAQ1Mod1/ai0")
            task.ai_channels.add_ai_accel_chan("cDAQ1Mod1/ai1")

            task.timing.cfg_samp_clk_timing(
                fre, source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=N)

            LSOL = b'\x5A\xF1\x02\x01\x05\x0A\x00\x5D'
            #RSOL = b'\x5A\xF1\x03\x01\x05\x0A\x00\x5E'
            self.s7.write(LSOL)
            #a=self.s7.read(16)
            #self.s7.write(RSOL)
            a=self.s7.read(16)
            
            print("Hitting done")
            value = task.read(N)
            print("Value read")
            v_ch0 = value[0]
            
            v_ch1 = value[1]

            number = sum(i > Triggering for i in v_ch0)
            print(number)
            if number == 0:
                print("No value found")

                return False
            else:
                task.close()

                print("Value found")
                position = next(x for x, val in enumerate(v_ch0)
                                if val > Triggering)
                print("position", position)

                first_index = int(position - pre_trig)
                last_index = int(first_index + Num_samples)

                print("f", first_index)
                print("l", last_index)

                channel1 = v_ch0[first_index:last_index]
                channel2 = v_ch1[first_index:last_index]

                # print("y",y)
                s = (len(channel1))
                s1 = len(channel2)
                print(s1)
                sample = list(range(s))
                signalDataA = {"sample": sample, "channel1": channel1, "channel2":channel2}
                self.__protocol.send_message('signalDataA', signalDataA)
            return True

        def istest2():
            
            number = 1

            task = nidaqmx.Task()
            

            task.ai_channels.add_ai_accel_chan("cDAQ1Mod1/ai0")
            task.ai_channels.add_ai_accel_chan("cDAQ1Mod1/ai1")

            task.timing.cfg_samp_clk_timing(
                fre, source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=N)

            

            #LSOL = b'\x5A\xF1\x02\x01\x05\x0A\x00\x5D'
            RSOL = b'\x5A\xF1\x03\x01\x05\x0A\x00\x5E'
            self.s7.write(RSOL)
            a=self.s7.read(16)
            
            #a=self.s7.read(16)
            
            print("Hitting done")
            value = task.read(N)
            print("Value read")
            v_ch0 = value[0]
            
            v_ch1 = value[1]

            number = sum(i > Triggering for i in v_ch1)
            print(number)
            if number == 0:
                print("No value found")

                return False
            else:
                task.close()

                print("Value found")
                position = next(x for x, val in enumerate(v_ch1)
                                if val > Triggering)
                print("position", position)

                first_index = int(position - pre_trig)
                last_index = int(first_index + Num_samples)

                print("f", first_index)
                print("l", last_index)

                channel1 = v_ch0[first_index:last_index]
                channel2 = v_ch1[first_index:last_index]

                # print("y",y)
                s = (len(channel1))
                s1 = len(channel2)
                print(s1)
                sample = list(range(s))
                signalDataB = {"sample": sample, "channel1": channel1, "channel2":channel2}
                self.__protocol.send_message('signalDataB', signalDataB)
            return True
        while True:
            t = istest()
            if t == True:
                
                t1=istest2()
                if t1==True:
                    break
                
    def start_front_stream(self):
        if self.__send_front_video:
            return  # ignore if already sending videos
        self.__send_front_video = True
        front = cv2.VideoCapture(0)
        front.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        front.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        front.set(cv2.CAP_PROP_FPS, 5)
        while (front.isOpened()):
            _, front_frame = front.read()
            img= cv2.resize(front_frame, (640,480))
            
            self.__protocol.send_message('front_frame',img)
            if not self.__send_front_video:
                front.release()
    

    def start_video_stream(self):
        if self.__send_video:
            return  # ignore if already sending videos
        self.__send_video = True
        def dsc(y_true, y_pred, smooth=1):
           y_true_f = K.flatten(y_true)
           y_pred_f = K.flatten(y_pred)
           intersection = tf.reduce_sum(y_true_f * y_pred_f)
           return (2. * intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + smooth)
        def dice_loss(y_true, y_pred):
           return 1.0 - dsc(y_true, y_pred)



        def IOU(y_true, y_pred):

            y_true = K.flatten(y_true)
            y_pred = K.flatten(y_pred)
            thresh = 0.5
            y_true = K.cast(K.greater_equal(y_true, thresh), 'float32')
            y_pred = K.cast(K.greater_equal(y_pred, thresh), 'float32')
            union = K.sum(K.maximum(y_true, y_pred)) + K.epsilon()
            intersection = K.sum(K.minimum(y_true, y_pred)) + K.epsilon()
            iou = intersection/union
            return iou

        def recall_m(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
            recall = true_positives / (possible_positives + K.epsilon())
            return recall

        def precision_m(y_true, y_pred):
            true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
            predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
            precision = true_positives / (predicted_positives + K.epsilon())
            return precision

        def f1_m(y_true, y_pred):
            precision = precision_m(y_true, y_pred)
            recall = recall_m(y_true, y_pred)
            return 2*((precision*recall)/(precision+recall+K.epsilon()))

        model = load_model('out.h5',custom_objects={'dice_loss':dice_loss,'IOU':IOU,'dsc':dsc,'precision_m':precision_m, 'recall_m':recall_m, 'f1_m':f1_m})

        vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        vid.set(cv2.CAP_PROP_FPS, 5)

        while (vid.isOpened()):
            _, frame = vid.read()
            print(frame.shape)
            frame=cv2.resize(frame, (512,512))
            
            
            small_img = cv2.resize(frame,(512,512))
            small_img = np.array(small_img)

            small_img = small_img[None, :, :, :]

            self.prediction = model.predict(small_img)[0] * 255
            
            bw=cv2.resize(self.prediction, (512,512))
            crack_image = cv2.resize(self.prediction,(512,512))
            b, g, r = cv2.split(crack_image)
            z = np.zeros_like(g)
            crack_image = cv2.merge((z, b, z))
           
            image2 = frame.astype(np.float32)

            result = cv2.addWeighted(image2, 0.5, crack_image, 0.5, 0)
            # result=result * 255
            result = result.astype(np.uint8)
            
            result=cv2.resize(result,(512,512))
            
            '''v=bytearray([183,184,1,4,1,197,198])
            self.s5.write(v)
            c=self.s5.read(10)
            array=[]
            for i in range (len(c)):
               b=c[i]
               i=i+1
               array.append(b)
            print(array)
            if (array[5]>=0 and array[6]>0 and array[7]>0 and array[8]>0):
                speed=array[5]+array[6]*256+array[7]*65536+array[8]*16777216
                print(speed)
            elif (array[5]>=0 and array[6]>0 and array[7]>0 and array[8]==0):
                speed=array[5]+array[6]*256+array[7]*65536
                print(speed)
            elif (array[5]>=0 and array[6]>0 and array[7]==0 and array[8]==0):
                speed=array[5]+array[6]*256
                print(speed)
            elif (array[5]>=0 and array[6]==0 and array[7]==00 and array[8]==0):
                speed=array[5]
                print(speed)
             
            alpha=0.0850340136
            a=speed*alpha
            if a!=0:
                a=round(a,2)
            a=str(a)
            b='CM'
            cm=a+b
            font=cv2.FONT_HERSHEY_PLAIN
            org=(3,20)
            fontscale=1
            color=(255,0,0)
            thickness=1
            result=cv2.putText(result,cm,org,font,fontscale,color,thickness,cv2.LINE_AA)'''

            self.__protocol.send_message('frame', result)
            self.__protocol.send_message('or_frame', frame)

            self.__protocol.send_message('bw_frame', bw)
            
            if not self.__send_video:
                vid.release()
    

    def SemiAuto(self):
        
        L_X=int((self.G_X/0.25)+1)
        L_Y=int(self.G_Y/0.25)

        for i in range(1,L_X+1):
        
            for j in range(1,L_Y+1):
                o,r,p=Video().detect()
                ta=262144
                rgb=p
                gray=cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
                _,binary=cv2.threshold(gray,25,255,cv2.THRESH_BINARY)
                
                Cbinary=binary.astype(np.uint8)
                contours, hierarchy=cv2.findContours(Cbinary,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                if (len(contours)==0):
                    Area=0
                    Density=0
                else:
                    a=[]
                    
                    for contour in contours:
                        area = cv2.contourArea(contour)
                        if area >40:
                            #num=cv2.contourArea(contour)
                            a.append(area)
                        else:
                            a.append(0)
                    Area=sum(a)
                    Density=(Area/ta)*100

                
                Density1="{:.2f}".format(Density)
                Area=str(Area)
                Density1=str(Density1)
                
                rec_x=i
                x=str(rec_x)
                if (i%2)==0:
                    rec_y=(L_Y-j)*0.25
                elif (i%2)!=0:
                    rec_y=j*0.25
                y=str(rec_y)
                b='M'
                M="Y="+y+b
                N="X="+x
                a="Area="+Area
                d="Density="+Density1+"%"
                P=N+","+M+","+a+","+d
                font=cv2.FONT_HERSHEY_PLAIN
                org=(3,20)
                fontscale=1
                color=(255,0,0)
                thickness=1
                
                r=cv2.putText(r,P,org,font,fontscale,color,thickness,cv2.LINE_AA)
                self.__protocol.send_message('frame', r)
                self.__protocol.send_message('or_frame', o)
                self.__protocol.send_message('bw_frame', p)
                if (Density>=0.1):
                    sample,channel1,channel2,channel11,channel22=eSignal(self.s7).signal()
                    AsignalDataA = {"sample": sample, "channel1": channel1, "channel2":channel2,"rec_x":rec_x,"rec_y":rec_y}
                    self.__protocol.send_message('AsignalDataA', AsignalDataA)
                    AsignalDataB = {"sample": sample, "channel11": channel11, "channel22":channel22,"rec_x":rec_x,"rec_y":rec_y}
                    self.__protocol.send_message('AsignalDataB', AsignalDataB)
                    up =b'\x5A\xF1\x01\x01\x36\xB0\x00\x33'
                    self.s7.write(up)
                    self.s7.read(16)
                    self.s7.write(up)
                    self.s7.read(16)
                    self.s7.write(up)
                    
                    X=[]
                    while True:
                        c=self.s7.read(16)
                        for k in range (len(c)):
                                    x=c[k]
                                    k=k+1
                                    X.append(x)
                        print(X)
                        if (len(X)==16):
                            print("done")
                            break

                    MotorDriver(self.s3,self.s4,self.s5,self.s6).moveForward(steps=294)
                
        
                else:
                    MotorDriver(self.s3,self.s4,self.s5,self.s6).moveForward(steps=294)
            if (i<L_X):    
                if (i%2)!=0:
                    MotorDriver(self.s3,self.s4,self.s5,self.s6).turnRight()
                    MotorDriver(self.s3,self.s4,self.s5,self.s6).moveForward(steps=294)
                    MotorDriver(self.s3,self.s4,self.s5,self.s6).turnRight1()
                elif (i%2)==0:
                    MotorDriver(self.s3,self.s4,self.s5,self.s6).turnLeft()
                    MotorDriver(self.s3,self.s4,self.s5,self.s6).moveForward(steps=294)
                    MotorDriver(self.s3,self.s4,self.s5,self.s6).turnLeft1()
            else:
                print("For loop Finished")

        print(self.G_X)
        if (self.G_X%1)!=0:
            print("Hello")
            MotorDriver(self.s3,self.s4,self.s5,self.s6).turnRight()
            OM=1176
            SF=OM*self.G_X
            MotorDriver(self.s3,self.s4,self.s5,self.s6).moveForward(steps=SF)
            MotorDriver(self.s3,self.s4,self.s5,self.s6).turnRight()
        elif (self.G_X%1)==0:
            print("Hi")
            MotorDriver(self.s3,self.s4,self.s5,self.s6).turnLeft()
            OM=1176
            SF=OM*self.G_X
            SFF=OM*self.G_Y
            MotorDriver(self.s3,self.s4,self.s5,self.s6).moveForward(steps=SF)
            MotorDriver(self.s3,self.s4,self.s5,self.s6).turnLeft()
            MotorDriver(self.s3,self.s4,self.s5,self.s6).moveForward(steps=SFF)
            MotorDriver(self.s3,self.s4,self.s5,self.s6).turnLeft()
            MotorDriver(self.s3,self.s4,self.s5,self.s6).turnLeft()





        feedData ="Done"
        self.__protocol.send_message('feedData', feedData)
        
            
        
        



    def forward(self):
        #print("Forward")
        #self.switch=bytearray([183,184,1,5,1,1,137])
        #self.s5.write(self.switch)
        '''self.s4.write(self.switch)
        self.s3.write(self.switch)
        self.s6.write(self.switch)'''
        self.s3.write(self.values35)
        self.s5.write(self.values35)
        self.s4.write(self.values46)
        self.s6.write(self.values46)

    def left(self):
        #print("Left")
        #self.switch=bytearray([183,184,1,5,1,1,137])
        #self.s5.write(self.switch)
        '''self.s4.write(self.switch)
        self.s3.write(self.switch)
        self.s6.write(self.switch)'''
        self.s3.write(self.values35)
        self.s5.write(self.values35)
        self.s4.write(self.values35)
        self.s6.write(self.values35)
        

    def right(self):
        #self.switch=bytearray([183,184,1,5,1,1,137])
        #print("Right")
        #self.s5.write(self.switch)
        '''self.s4.write(self.switch)
        self.s3.write(self.switch)
        self.s6.write(self.switch)'''
        self.s3.write(self.values46)
        self.s5.write(self.values46)
        self.s4.write(self.values46)
        self.s6.write(self.values46)

    def back(self):
        self.switch=bytearray([183,184,1,5,1,1,137])
        #print("Back")
        #self.s5.write(self.switch)
        '''self.s4.write(self.switch)
        self.s3.write(self.switch)
        self.s6.write(self.switch)'''
        self.s3.write(self.values46)
        self.s5.write(self.values46)
        self.s4.write(self.values35)
        self.s6.write(self.values35)

    def stop(self):
        #print("Stop")
       # self.switch=bytearray([183,184,1,5,1,1,137])
        #self.s5.write(self.switch)
        '''self.s4.write(self.switch)
        self.s3.write(self.switch)
        self.s6.write(self.switch)'''
        self.s3.write(self.values)
        self.s5.write(self.values)
        self.s4.write(self.values)
        self.s6.write(self.values)
        
        





if __name__ == "__main__":
    
    server = Server()
    
    server.serve_forever()  # This method will block the thread. That's why it must be put at the end.
