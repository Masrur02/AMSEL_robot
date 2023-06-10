import time
import io
import serial
import imutils
from serial import Serial
import select
import math
from threading import Thread
from threading import Lock
import asyncio
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow import keras
from tensorflow.keras.models import load_model
import tensorflow.keras.backend as K
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
DIR_POSITIVE = 1
DIR_NEGATIVE = -1



class Motor(Serial):
    def __init__(self, port, baudrate=19200, direction=DIR_POSITIVE,write_timeout=0):
        super().__init__(port=port, baudrate=baudrate)
        self.__direction  = direction



    def readPosition(self):
        v=bytearray([183,184,1,4,1,197,198])

        self.write(v)

        c_p=self.read(10)

        array=[]
        for i in range (len(c_p)):
            b=c_p[i]
            i=i+1
            array.append(b)


        if (array[8]==0):
            if (array[5]>=0 and array[6]>0 and array[7]>0 and array[8]>0):
                c_p=array[5]+array[6]*256+array[7]*65536+array[8]*16777216

            elif (array[5]>=0 and array[6]>0 and array[7]>0 and array[8]==0):
                c_p=array[5]+array[6]*256+array[7]*65536

            elif (array[5]>=0 and array[6]>0 and array[7]==0 and array[8]==0):
                c_p=array[5]+array[6]*256

            elif (array[5]>=0 and array[6]==0 and array[7]==00 and array[8]==0):
                c_p=array[5]

        elif (array[8]==255):
            if (array[5]<=255 and array[6]==255 and array[7]==255 and array[8]==255): 
                c_p=-(256-array[5])
            elif (array[5]<=255 and array[6]<255 and array[7]==255 and array[8]==255):
                c_p=((256-array[6])*256)-(array[5])
                c_p=-(c_p)
            elif (array[5]<=255 and array[6]<255 and array[7]<255 and array[8]==255):
                c_p=(256-array[7]*65536)-(array[6]*256)-array[5]
                c_p=-(c_p)

        return c_p
        #




    def targetPosition(self):
        if (self.targetPos>=0):

            if self.targetPos<=255:
                D1=self.targetPos
                D2=0 
                D3=0
                D4=0
            elif 255<self.targetPos<65536:
                D1=self.targetPos%256
                D2=self.targetPos/256
                D2=math.floor(D2)
                D3=0
                D4=0
            elif 65536<=self.targetPos<16777216:
                D1=self.targetPos%256
                b=self.targetPos/256
                D2=b%256
                D2=math.floor(D2)
                D3=math.floor(b/256)
                D4=0
        if (self.targetPos<0):

            if self.targetPos>=-255:
                self.targetPos=abs(self.targetPos)
                D1=256-self.targetPos
                D2=255 
                D3=255
                D4=255
            elif -255>self.targetPos>-65536:

                self.targetPos=abs(self.targetPos)
                if (self.targetPos%256)==0:
                    D1=0
                else:
                    D1=256-(self.targetPos%256)
                D2=255-(self.targetPos/256)
                D2=math.ceil(D2)
                D3=255
                D4=255


            elif -65536>=self.targetPos>-16777216:
                self.targetPos=abs(self.targetPos)
                if (self.targetPos%256)==0:
                    D1=0
                else:
                    D1=256-(self.targetPos%256)

                b=self.targetPos/256
                D2=255-(b%256)
                D2=math.ceil(D2)
                D3=255-(b/256)
                D3=math.ceil(D3)
                D4=255

        return D1,D2,D3,D4

    def checkSum(self):
        one=bin(1)

        Sumbin=bin(self.sum)

        SumBin=Sumbin[-8:]


        def onescomplement(a):
            b=''
            for i in a:

                i=1-int(i)
                i=str(i)

                b+=i

            return b
        SumCom=onescomplement(SumBin)


        SumChk=bin(int(SumCom, 2) + int(one, 2))

        SumChk=int(SumChk,2)
        return SumChk 


    def checkPosition(self):
        self.speed=[]
        s=bytearray([183,184,1,4,1,197,198])
        self.write(s)
        c_s=self.read(10)
        for k in range (len(c_s)):
                x=c_s[k]
                k=k+1
                self.speed.append(x)
        return self.speed



    def sendPosition(self,value):


        self.currPos=self.readPosition()


        self.targetPos=self.currPos+(value*self.__direction)
        self.targetPos=int(self.targetPos)

        self.D1,self.D2,self.D3,self.D4=self.targetPosition()

        self.sum=183+184+1+243+4+self.D1+self.D2+self.D3+self.D4
        self.chk=self.checkSum()
        if (self.chk>255):
            self.chk=0

        #print(self.D1,self.D2,self.D3,self.D4,self.chk)
        self.switch=bytearray([183,184,1,5,1,1,137])
        self.write(self.switch)

        self.pos=bytearray([183,184,1,243,4,self.D1,self.D2,self.D3,self.D4,self.chk])

        self.write(self.pos)





        while True:
            chkPos=self.checkPosition()
            if (chkPos[5]==self.D1 and chkPos[6]==self.D2 and chkPos[7]==self.D3 and chkPos[8]==self.D4):
                break
            else:
                continue






class MotorDriver:
    def __init__(self, s3, s4, s5, s6):
        self.__s3=s3
        self.__s4=s4
        self.__s5=s5
        self.__s6=s6
        self.__all_motors  = [self.__s3, self.__s4, self.__s5, self.__s6]

    def moveForward(self, steps):
        threads = []
        for motor in self.__all_motors:
            t = Thread(target = motor.sendPosition, args=(steps,))
            threads.append(t)
            t.daemon = True

            t.start()
        for t in threads:
            t.join()

    def movebackward(self, steps):
        threads = []
        for motor in self.__all_motors:
            t = Thread(target = motor.sendPosition, args=(steps,))
            threads.append(t)
            t.daemon = True
            t.start()
        for t in threads:
            t.join()

    def turnRight(self):
        threads = []
        steps = [-862, 870, -818, 863]
        for motor, pos in zip(self.__all_motors, steps):
            t = Thread(target = motor.sendPosition, args=(pos,))
            threads.append(t)
            t.daemon = True
            t.start()
        for t in threads:
            t.join()
    def turnRight1(self):
        threads = []
        steps = [-862, 870, -818, 863]
        for motor, pos in zip(self.__all_motors, steps):
            t = Thread(target = motor.sendPosition, args=(pos,))
            threads.append(t)
            t.daemon = True
            t.start()
        for t in threads:
            t.join()

    def turnLeft(self):
        threads = []
        steps = [1011, -862, 832, -858]
        for motor, pos in zip(self.__all_motors, steps):
            t = Thread(target = motor.sendPosition, args=(pos,))
            threads.append(t)
            t.daemon = True
            t.start()
        for t in threads:
            t.join()

    def turnLeft1(self):
        threads = []
        steps = [1011, -862, 832, -858]
        for motor, pos in zip(self.__all_motors, steps):
            t = Thread(target = motor.sendPosition, args=(pos,))
            threads.append(t)
            t.daemon = True
            t.start()
        for t in threads:
            t.join()

class Video():




    def detect(self):
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
        vid = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
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
        return frame,result,self.prediction



class eSignal:
    def __init__(self, s7):

        self.__s7=s7


    def signal(self):
        down = b'\x5A\xF1\x01\x00\x36\xB0\x00\x32'
        self.__s7.write(down)
        c=self.__s7.read(16)
        self.__s7.write(down)
        c=self.__s7.read(16)
        self.__s7.write(down)

        X=[]
        while True:
            c=self.__s7.read(16)
            for k in range (len(c)):
                        x=c[k]
                        k=k+1
                        X.append(x)
            print(X)
            if (len(X)==16):
                print("done")
                break

        t_ms = 500


        Triggering = float(0.5)
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
            self.__s7.write(LSOL)
            #a=self.s7.read(16)
            #self.s7.write(RSOL)
            a=self.__s7.read(16)

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

                self.channel1 = v_ch0[first_index:last_index]
                self.channel2 = v_ch1[first_index:last_index]

                # print("y",y)
                s = (len(self.channel1))
                s1 = len(self.channel2)
                print(s1)
                self.sample = list(range(s))
                #signalDataA = {"sample": self.sample, "channel1": self.channel1, "channel2":self.channel2}
                #self.__protocol.send_message('signalDataA', signalDataA)
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
            self.__s7.write(RSOL)
            a=self.__s7.read(16)

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

                self.channel11 = v_ch0[first_index:last_index]
                self.channel22 = v_ch1[first_index:last_index]

                # print("y",y)
                s = (len(self.channel11))
                s1 = len(self.channel22)
                print(s1)
                self.sample = list(range(s))
                #signalDataB = {"sample": sample, "channel1": channel1, "channel2":channel2}
                #self.__protocol.send_message('signalDataB', signalDataB)
            return True
        while True:
            t = istest()
            if t == True:

                t1=istest2()
                if t1==True:
                    break
        return self.sample,self.channel1,self.channel2,self.channel11,self.channel22 
