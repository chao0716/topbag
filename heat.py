# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:37:04 2019

@author: chaoz
"""

import cv2   
import numpy as np
from PIL import Image
import os


mix_dirlist=[]
total_sc=0
image_dir='C:\\Users\\chaoz\\Desktop\\(3+2)1123'
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
    if os.path.exists(xml_dir)==True:     
        rgb_img = cv2.imread(RGB_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)      
        depth_img = cv2.imread(depth_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        depth_img=depth_img.astype(int)
        depth_img=np.uint8(depth_img)
        #im=im[50:800,200:1080]
#        min_exclude_0=depth_img[depth_img!=0].min()
#        max_exclude_0=depth_img[depth_img!=0].max()
#        diff = max_exclude_0 - min_exclude_0
#        is0=np.where(depth_img!=0)
#        depth_img[is0]=depth_img[is0]-min_exclude_0
#        depth_img[is0]=depth_img[is0]*255
#        depth_img[is0]=depth_img[is0]/diff
#        depth_img=depth_img.reshape((960,1280))
#        for i in range (np.shape(depth_img)[0]):
#            for j in range(np.shape(depth_img)[1]):
#                if depth_img[i,j]!=0:
#                    depth_img[i,j]=(depth_img[i,j]-min_exclude_0)*255/diff
        depth_img[np.where(depth_img==0)]=255
        #save image
        r = Image.fromarray(np.uint8(depth_img))
        g = Image.fromarray(np.uint8(depth_img))
        b = Image.fromarray(np.uint8(depth_img))
        image = Image.merge("RGB", (r, g, b))
        image.save(RGB_dir.split('_')[0]+'_heat.png')
        mix_dirlist.append(RGB_dir.split('_')[0]+'_mix.png')