# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 20:44:17 2018

@author: chaoz
"""

import cv2   
import numpy as np
from PIL import Image
import os


mix_dirlist=[]
total_sc=0
#image_dir='C:\\Users\\chaoz\\Desktop\\(3+2)1123'
image_dir='C:\\Users\\chaoz\\Desktop\\1121-3+2'
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
    if os.path.exists(xml_dir)==True:     
        rgb_img = cv2.imread(RGB_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)      
        depth_img = cv2.imread(depth_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        depth_img = (depth_img - np.min(depth_img)) / (np.max(depth_img) - np.min(depth_img)) *255

        kernel = np.ones((7, 7), np.uint8)
        depth_img =cv2.morphologyEx(depth_img, cv2.MORPH_CLOSE, kernel)
        depth_img[np.where(depth_img==0)]=255
        #save image
        r = Image.fromarray(np.uint8(depth_img))
        g = Image.fromarray(np.uint8(rgb_img[:,:,1]))
        b = Image.fromarray(np.uint8(rgb_img[:,:,2]))
        image = Image.merge("RGB", (r, g, b))
        image.save(RGB_dir.split('_')[0]+'_mix.png')
        mix_dirlist.append(RGB_dir.split('_')[0]+'_mix.png')