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


import tensorflow as tf
from tensorflow import keras
from tensorflow import keras
from tensorflow.keras.models import load_model
import tensorflow.keras.backend as K



# Load Keras model


class Server:
    def __init__(self):
        self.__send_video = False
        self.__send_front_video = False
        message_handlers = {
            'command': self.commandHandler,
            'button': self.onButtonClick,
            'triggerData': self.onTriggerData,
            'speedData': self.onSpeedData
        }
        self.__protocol = Protocol(on_message_handlers=message_handlers)

    def commandHandler(self, command):
        commands = {
            'end_video': self.onEndVideo,
            'start_video': self.onStartVideo,
            "start_front_video":self.onFrontVideo,
            'end_front_video': self.offFrontVideo,
            "startSignal": self.onSignal,
            'autonomous': self.onAutonomous,
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

    def onFrontVideo(self):
        thread = Thread(target=self.start_front_stream)
        thread.start()

    def onStartVideo(self):
        thread = Thread(target=self.start_video_stream)
        thread.start()

    def onSignal(self):
        thread = Thread(target=self.startSignal)
        thread.start()

    def onTriggerData(self, triggerData):
        Thread(target=self.onTrigger, args=(triggerData,)).start()

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

    def offFrontVideo(self):
        self.__send_front_video = False

    def onTrigger(self, triggerData):
        self.time = triggerData.get("time")
        self.trigger = triggerData.get("trigger")

    def onSpeed(self, speedData):
        self.speed = speedData.get("speed")
        print(self.speed)
        self.speed1=self.speed*4

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

            value = task.read(N)

            v_ch0 = value[0]
            v_ch1 = value[1]

            number = sum(i > Triggering for i in v_ch0)

            if number == 0:
                print("No value found")

                return False
            else:
                task.close()

                #print("Value found")
                position = next(x for x, val in enumerate(v_ch0)
                                if val > Triggering)
                print("position", position)

                first_index = int(position - pre_trig)
                if first_index <0:
                    print("No value found")
                    return False
                else :
                    #print("Value found")
                    last_index = int(first_index + Num_samples)
                    if last_index > (N-pre_trig):
                        print("No value found")
                        return False
                    else:
                        
                        print("Value found")
                        print("f", first_index)
                        print("l", last_index)

                        y = v_ch0[first_index:last_index]
                        y1 = v_ch1[first_index:last_index]

                        # print("y",y)
                        s = (len(y))
                        s1 = len(y1)
                        print(s1)
                        X = list(range(s))
                        signalData = {"X": X, "y": y, "y1":y1}
                        self.__protocol.send_message('signalData', signalData)



                        return True
        while True:
            t = istest()
            if t == True:
                break
                
    def start_front_stream(self):
        if self.__send_front_video:
            return  # ignore if already sending videos
        self.__send_front_video = True
        front = cv2.VideoCapture(1)
        front.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
        front.set(cv2.CAP_PROP_FRAME_HEIGHT, 160)
        front.set(cv2.CAP_PROP_FPS, 25)
        while (front.isOpened()):
            _, front_frame = front.read()
            img= cv2.resize(front_frame, (512, 512))
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

            iou = intersection / union

            return iou
        model = load_model('C:/Users/ASMEL/Desktop/Robot/unew_3.h5', custom_objects={'dice_loss': dice_loss, 'IOU': IOU, 'dsc': dsc})

        vid = cv2.VideoCapture(0)
        vid.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 160)
        vid.set(cv2.CAP_PROP_FPS, 25)

        while (vid.isOpened()):
            _, frame = vid.read()
            small_img = cv2.resize(frame, (512, 512))
            small_img = np.array(small_img)

            small_img = small_img[None, :, :, :]

            prediction = model.predict(small_img)[0] * 255
            crack_image = cv2.resize(prediction, (640, 480))
            b, g, r = cv2.split(crack_image)
            z = np.zeros_like(g)
            crack_image = cv2.merge((z, b, z))

            image2 = frame.astype(np.float32)

            result = cv2.addWeighted(image2, 0.5, crack_image, 0.5, 0)
            # result=result * 255
            result = result.astype(np.uint8)
            self.__protocol.send_message('frame', result)
            if not self.__send_video:
                vid.release()

    def forward(self):
        print("Forward")

        s.write(str.encode("vc1={speed}\n".format(speed=self.speed1)))
        s.write(str.encode("vc2={speed}\n".format(speed=self.speed)))

    def left(self):
        print("Left")

        s.write(str.encode("vc1=-{speed}\n".format(speed=self.speed1)))
        s.write(str.encode("vc2={speed}\n".format(speed=self.speed)))

    def right(self):
        print("Right")

        s.write(str.encode("vc1={speed}\n".format(speed=self.speed1)))
        s.write(str.encode("vc2=-{speed}\n".format(speed=self.speed)))

    def back(self):
        print("Back")

        s.write(str.encode("vc1=-{speed}\n".format(speed=self.speed1)))
        s.write(str.encode("vc2=-{speed}\n".format(speed=self.speed)))

    def stop(self):
        print("Stop")

        s.write(str.encode("vc1=0\n"))
        s.write(str.encode("vc2=0\n"))


if __name__ == "__main__":
    s = Serial('COM3', 115200)
    s.flush()
    server = Server()
    server.serve_forever()  # This method will block the thread. That's why it must be put at the end.
