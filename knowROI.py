# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:54:07 2019

@author: chaoz
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:20:46 2019

@author: chaoz
"""

import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import heapq
only1=0
kdanfkn=0
total_sc=0
image_dir='C:\\Users\\chaoz\\Desktop\\1121-3+2'
sname='RGB.png'
dname='D.png'
xmlname='xml'
RGB_dirlist=[]
depth_dirlist=[]
xml_dirlist=[]
for dire in os.listdir(image_dir):
    pwd_dir=os.path.join(image_dir,dire)
    if sname in os.path.split(pwd_dir)[1]:
        RGB_dirlist.append(pwd_dir) 
    if xmlname in os.path.split(pwd_dir)[1]:
        xml_dirlist.append(pwd_dir)
    if dname in os.path.split(pwd_dir)[1]:
        depth_dirlist.append(pwd_dir)
        
for de in range(len(depth_dirlist)):
#    print(de)
    depth_dir=depth_dirlist[de]
    RGB_dir=RGB_dirlist[de]
    
    bag1_xmin=[]
    bag1_ymin=[]
    bag1_xmax=[]
    bag1_ymax=[]
    bag1_count=0
    bag2_xmin=[]
    bag2_ymin=[]
    bag2_xmax=[]
    bag2_ymax=[]
    bag2_count=0
    xml_dir=RGB_dir.split('.')[0]+'.xml'
    if os.path.exists(xml_dir)==True: 
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        for member in root.findall('object'):
            if member[0].text=='bag1':
                bag1_count+=1
                bag1_xmin.append(int(member[4][0].text))
                bag1_ymin.append(int(member[4][1].text))
                bag1_xmax.append(int(member[4][2].text))
                bag1_ymax.append(int(member[4][3].text))
            if member[0].text=='bag2':
                bag2_count+=1
                bag2_xmin.append(int(member[4][0].text))
                bag2_ymin.append(int(member[4][1].text))
                bag2_xmax.append(int(member[4][2].text))
                bag2_ymax.append(int(member[4][3].text))


        depth_image_path=depth_dir
        depth_image = np.array(cv2.imread(depth_image_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))
        depth_image = depth_image[100:750,200:1080]
        x=depth_image

        x = (x - np.min(x)) / (np.max(x) - np.min(x)) *255
#        x = cv2.fastNlMeansDenoisingColored(x,None,10,10,7,21)
        kernel = np.ones((7, 7), np.uint8)
        x =cv2.morphologyEx(x, cv2.MORPH_CLOSE, kernel)
        im = x       
        im[np.where(im==0)]=255
#        iii = np.unravel_index(np.argmin(im), im.shape)
        ii = np.unravel_index(np.argsort(im.ravel()), im.shape)
        
        RGB_im=cv2.imread(RGB_dir, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        RGB_im = RGB_im[100:750,200:1080]
        idx = 0
        n = 500
        for i in range(n):
#            print(ii[0][i], ii[1][i], im[ii[0][i], ii[1][i]], sorted(im.ravel())[i])
            cv2.circle(RGB_im, (ii[1][i],ii[0][i]), 5, (0, 0, int(i/n*255)), -8)
                
#        cv2.imshow('t', RGB_im)
#        cv2.waitKey(10)
        cv2.imwrite(RGB_dir+".jpg", RGB_im)
#        cv2.imwrite(RGB_dir+"_1.jpg", )
     
                     