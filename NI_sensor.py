# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 20:35:11 2021

@author: almas
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 19:19:23 2021

@author: almas
"""




import matplotlib.pyplot as plt
import time
import nidaqmx
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge, Slope
from nidaqmx.constants import AcquisitionType
import pandas as pd
def istest():
    number = 1

    t_ms = 100

    t_s = .001*t_ms
    fre = 30000
    Num_samples = int(t_s*fre)

    N = 100000
    pre = 10
    pre_trig = int(10/100*Num_samples)

    Triggering = 0.2

    task = nidaqmx.Task()
    
    task.ai_channels.add_ai_accel_chan("cDAQ1Mod1/ai0")
    task.ai_channels.add_ai_accel_chan("cDAQ1Mod1/ai2")
    
    task.timing.cfg_samp_clk_timing(
        fre, source="", active_edge=Edge.RISING, sample_mode=AcquisitionType.FINITE, samps_per_chan=N)
    
    value = task.read(N)
    
    
    v_ch0=value[0]
    v_ch1=value[1]
    
    number = sum(i > Triggering for i in v_ch0)
   

    if number == 0:
        print("No value found")

        return False
    else:
        task.close()
        
        print("Value found")
        position = next(x for x, val in enumerate(v_ch0)
                        if val > Triggering)
        print("position", position)
        
        
        
        
        first_index = int(position-pre_trig)
        last_index = int(first_index+Num_samples)
        
        print("f",first_index)
        print("l",last_index)
        
        y = v_ch0[first_index:last_index]
        y1=v_ch1[first_index:last_index]

        # print("y",y)
        s = (len(y))
        s1=len(y1)
        print(s1)
        X = list(range(s))
        # print(X)
        # print(type(X))
        # print(type(y))

        plt.subplot(2, 1, 1)
        plt.plot(X, y, 'b-')
        plt.title('Channel1')
        plt.xlabel('samples')
        plt.ylabel('value')


        plt.subplot(2, 1, 2)
        plt.plot(X, y1, 'r-')
        plt.title('Channel2')
        plt.xlabel('samples')
        plt.ylabel('value')

        plt.show()
        print(len(y))
        print(len(y1))
        #print(y1)
        dic1 = {'X': X, 'value': y}
        dic2 = {'X': X, 'value': y1}
        df1 = pd.DataFrame(dic1)
        df2 = pd.DataFrame(dic2)
        df1.to_csv('channel1.csv', index=False)
        df2.to_csv('channel2.csv', index=False)
        
        return True


def isnew():
    while True:
        t = istest()
        if t == True:
            break


isnew()
