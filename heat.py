# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:37:04 2019

@author: chaoz
"""

import cv2   
import numpy as np
from PIL import Image
import os
import numpy.random
import matplotlib.pyplot as plt

depth_img = np.array(cv2.imread('dd.png',cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))
plt.imshow(depth_img)
roi = np.array(cv2.imread('rr.png',cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))

min_d=np.min(roi[np.where(roi!=0)])
max_d=np.max(roi[np.where(roi!=0)])
depth_img[np.where(depth_img<min_d)]=min_d
depth_img[np.where(depth_img>max_d)]=max_d
depth_img = (depth_img - min_d) / 3000 *255 
plt.imshow(depth_img)



mix_dirlist=[]
total_sc=0
image_dir='C:\\Users\\chaoz\\Desktop\\trainset\\'
#image_dir='C:\\Users\\chaoz\\Desktop\\1121-3+2'
sname='RGB.png'
RGB_dirlist=[]
depth_dirlist=[]
xml_dirlist=[]
for dire in os.listdir(image_dir):
    pwd_dir=os.path.join(image_dir,dire)
    if sname in os.path.split(pwd_dir)[1]:
        RGB_dirlist.append(pwd_dir) 

xml_list = []
for i in range(len(RGB_dirlist)):
    print(i/len(RGB_dirlist))
    RGB_dir=RGB_dirlist[i]
    depth_dir=RGB_dir.split('_')[0]+'_D.png'
    xml_dir=RGB_dir.split('.')[0]+'.xml'
    if os.path.exists(xml_dir)==False:     
        rgb_img = cv2.imread(RGB_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)      
        depth_img = cv2.imread(depth_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        depth_img = depth_img[80:850,170:1130]
        print(np.min(depth_img[np.where(depth_img!=0)]),np.max(depth_img),np.mean(depth_img))
#        depth_img = cv2.resize(depth_img, (200,200))

        x=depth_img

        x = (x - np.min(x)) / (np.max(x) - np.min(x)) *255
#        x = cv2.fastNlMeansDenoisingColored(x,None,10,10,7,21)
        kernel = np.ones((7, 7), np.uint8)
        x =cv2.morphologyEx(x, cv2.MORPH_CLOSE, kernel)
        ada=np.where(x>=0) and np.where(x<100)
        x[ada]=np.nan
        xdx=np.where(x>190)
        x[xdx]=np.nan
        #X = np.int8(X) 
        plt.imshow(x)  
        plt.colorbar()        
#        plt.savefig(RGB_dir.split('_')[0]+'_heat.png')
        plt.show() 