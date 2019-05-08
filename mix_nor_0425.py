# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:05:03 2019

@author: chaoz
"""

import cv2   
import numpy as np
from PIL import Image
import os


mix_dirlist=[]
total_sc=0
image_dir='C:\\Users\\chaoz\\Desktop\\testset\\'
save_dir='C:\\Users\\chaoz\\Desktop\\0417_6000_false\\'
xml_floder='C:\\Users\\chaoz\\Desktop\\testxml\\'
sname='RGB.png'
RGB_dirlist=[]
depth_dirlist=[]
xml_dirlist=[]
for dire in os.listdir(image_dir):
    if sname in os.path.split(dire )[1]:
        RGB_dirlist.append(dire ) 

xml_list = []
for i in range(len(RGB_dirlist)):
    print(i/len(RGB_dirlist))
    RGB_dir=os.path.join(image_dir,RGB_dirlist[i])    
    depth_dir=RGB_dir.split('_')[0]+'_D.png'
    roi_dir=RGB_dir.split('_')[0]+'_D_ROI.png'
    xml_dir=xml_floder+RGB_dirlist[i].split('_')[0]+'_RGB.xml'
    if os.path.exists(xml_dir)==True:     
        rgb_img = cv2.imread(RGB_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)      
        depth_img = cv2.imread(depth_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        roi = np.array(cv2.imread(roi_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))
        min_d=np.min(roi[np.where(roi!=0)])
        max_d=np.max(roi[np.where(roi!=0)])
        depth_img[np.where(depth_img<min_d)]=min_d
        depth_img[np.where(depth_img>max_d)]=max_d
        depth_img = (depth_img - min_d) / 3000 *255

        kernel = np.ones((7, 7), np.uint8)
        depth_img =cv2.morphologyEx(depth_img, cv2.MORPH_CLOSE, kernel)
#        depth_img[np.where(depth_img==0)]=255
        #save image
        r = Image.fromarray(np.uint8(depth_img))
        g = Image.fromarray(np.uint8(rgb_img[:,:,1]))
        b = Image.fromarray(np.uint8(rgb_img[:,:,2]))
        image = Image.merge("RGB", (r, g, b))
        image.save(save_dir+RGB_dirlist[i].split('_')[0]+'_mix.png')