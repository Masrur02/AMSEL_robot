# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 10:17:55 2022

@author: Khan
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 13:01:26 2022

@author: Khan
"""

import cv2
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import cv2
import numpy as np
  
im = cv2.imread('e.png')
im=cv2.resize(im, (640,480), interpolation = cv2.INTER_AREA)
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray,100, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



n=0
ont = cv2.FONT_HERSHEY_SIMPLEX
fontScale =0.8
color = (0, 0,255)
thickness = 1


font = cv2.FONT_HERSHEY_SIMPLEX
n=0
Area=[]

Length=[]
sz=640*480


for contour in contours:
    
    
    
    area = cv2.contourArea(contour)
    if area>120:
        area2 = cv2.contourArea(contour)
        Area.append(area2)
        contour2=contour[:, 0].astype(int)
        
        
        
        ###########Width Calculation#########
        contour = pd.DataFrame(contour2)
        
        awa = contour.groupby([0]).count()
        awb = contour.groupby([1]).count()
        awa.reset_index(inplace=True)
        awb.reset_index(inplace=True)
        c=awa[0]
        c1=awb[1]
        
        if len(awa)>len(awb):
            Widths=[]
        
           
            
            
            for i in c: 
               
                width=[]
                
               
                for j in range (len(contour2)):
                        if contour2[j:j+1,0:1]==i:
                            width.append(int(contour2[j:j+1,1:2]))
                            
                            a=min(width)
                            b=max(width)
                        
                        
                            
                        
                        
                #        
                # 
                # i=i+1
                Widths.append(b-a) 
            
            Max_width=max(Widths)
            ind=Widths.index(Max_width)
            cols=c[ind]
                        
            occurs=[]
            
            
            #for i in cols:
            for j in range(len(contour2)):
                    
               
                    if contour2[j:j+1,0:1]==cols:
                       
                        occurs.append(int(contour2[j:j+1,1:2]))
            min_pos=min(occurs)
            max_pos=max(occurs)
            #Width.append(max_pos- min_pos +1)
                        
            
            ########### Drawing number#################
            
            n=n+1
            N= cv2.moments(contour2)
            cx= int(N['m10']/N['m00'])
            cy= int(N['m01']/N['m00'])
            
            
            
            ############ Drawing line ###################
            line_thickness = 2
            new = cv2.putText(im, str(n), (cy+1,cx+1), font, 
                       fontScale, color, thickness, cv2.LINE_AA)
            
            new=cv2.line(im, (cols,min_pos), (cols,max_pos), (255,0, 0), thickness=line_thickness)
            
            
            
            ######### Length Calculation########
              
            start_x=int(min(contour2[:,-1]))
          
            finish_x=int(max(contour2[:,-1]))
            
            start_y=int(min(contour2[:,0]))
          
            finish_y=int(max(contour2[:,0]))
            
           
            
            l= ((((finish_x - start_x )**2) + ((finish_y-start_y)**2) )**0.5)
            print(l)
            Length.append(l)
        else:
            
            Widths=[]
            
            
            
            for i in c1: 
               
                width=[]
                
               
                for j in range (len(contour2)):
                        if contour2[j:j+1,1:2]==i:
                            width.append(int(contour2[j:j+1,0:1]))
                            
                            a=min(width)
                            b=max(width)
                        
                        
                            
                        
                        
                #        
                # 
                # i=i+1
                Widths.append(b-a) 
            
            Max_width=max(Widths)
            ind=Widths.index(Max_width)
            rows=c1[ind]
            occurs=[]
            
            #for i in cols:
            for j in range(len(contour2)):
                    
               
                    if contour2[j:j+1,1:2]==rows:
                       
                        occurs.append(int(contour2[j:j+1,0:1]))
            min_pos=min(occurs)
            max_pos=max(occurs)
            
                        
            
            ########### Drawing number#################
            
            n=n+1
            N= cv2.moments(contour2)
            cx= int(N['m10']/N['m00'])
            cy= int(N['m01']/N['m00'])
            
            
            
            ############ Drawing line ###################
            line_thickness = 2
            new = cv2.putText(im, str(n), (cy+1,cx+1), font, 
                       fontScale, color, thickness, cv2.LINE_AA)
            
            new=cv2.line(im, (min_pos,rows), (max_pos,rows), (255,0, 0), thickness=line_thickness)
            
            
            
            ######### Length Calculation########
              
            start_x=int(min(contour2[:,-1]))
          
            finish_x=int(max(contour2[:,-1]))
            
            start_y=int(min(contour2[:,0]))
          
            finish_y=int(max(contour2[:,0]))
            
           
            
            l= ((((finish_x - start_x )**2) + ((finish_y-start_y)**2) )**0.5)
            print(l)
            Length.append(l)
            
            
cv2.drawContours(im, contours, -1, (0, 255, 0),1)

cv2.imshow('Contours', im)
cv2.imwrite("p1.png",im)

T_Area=sum(Area)
Density=(T_Area/sz)*100    
print("length",Length)  
print("Max_width",Max_width) 
print("Area",Area)     
print("Total Area",T_Area)  
print("Density",Density)  
cv2.waitKey(0)
cv2.destroyAllWindows()
