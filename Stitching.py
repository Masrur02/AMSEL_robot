from PIL import Image,ImageOps
import os, sys

import numpy as np
import matplotlib.pyplot as plt

from glob import glob
import cv2


path = "P"
dirs = os.listdir( path )
dirs.sort()
x_train=[]

n=4

file_name=glob(path+"/*jpg")


j=1
for file in file_name:
        print(j)
        im=cv2.imread(file)
        im =cv2.resize(im, (512,512), interpolation = cv2.INTER_AREA)
        
       
        x_train.append(im)
        j=j+1




chunks = [x_train[x:x+n] for x in range(0, len(x_train), n)]



tmerged=[]

for i in range (len(chunks)):
    merged=[]
    
    if (i==0):
        chunks[i]=list(reversed(chunks[i]))
        
    elif (i==1):
        chunks[i]=chunks[i]
        
        
    elif (i%2==0):
        chunks[i]=list(reversed(chunks[i]))
        
        
    else:
        chunks[i]=chunks[i]
        
        
        
        
        
        
    for j, img in enumerate(chunks[i]):
        img=np.array(img)
       
        merged.append(img)

    merge = np.concatenate(merged)
    
    
    
    
   
    
    
    
    
    tmerged.append(merge)

tmerge = np.concatenate(tmerged,axis=1)
#tmerge=np.flip(tmerge, axis=1)
plt.imshow(tmerge)
#im1 = tmerge.size((1280,700))
im1 = cv2.imwrite("grid.jpg",tmerge)   












            
            
            
            
        
    
        
        
    
    
    
 


















