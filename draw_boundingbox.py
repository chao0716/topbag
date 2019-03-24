# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:51:06 2019

@author: chaoz
"""

import xml.etree.ElementTree as ET
import cv2
import os
import numpy as np

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

for i in range(len(RGB_dirlist)):
    print(i,i/len(RGB_dirlist))
    RGB_dir=RGB_dirlist[i]
    depth_dir=depth_dirlist[i]
    xml_dir=RGB_dir.split('.')[0]+'.xml'
    if os.path.exists(xml_dir)==True:       
        tree = ET.parse(xml_dir)
        rect={}
        line=""
        root = tree.getroot()
        rgb_image = np.array(cv2.imread(RGB_dir, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))
        #open image before draw
#        depth_image_path=depth_dir
#        depth_image = np.array(cv2.imread(depth_image_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))
#        
#        im=depth_image.astype(int)
#        min_exclude_0=im[im!=0].min()
#        max_exclude_0=im[im!=0].max()
#        
#        diff = max_exclude_0 - min_exclude_0
#        
#        
#        for i in range (np.shape(im)[0]):
#            for j in range(np.shape(im)[1]):
#                if im[i,j]!=0:
#                    im[i,j]=(im[i,j]-min_exclude_0)*255/diff
#
#        im[np.where(im==0)]=255
#        im2=im
#        im3=im
#        im2=np.concatenate((im,im2),axis=1)
#        im3=np.concatenate((im2,im3),axis=1)
        
        img=rgb_image
        for ob in root.iter('object'): 
            if ob[0].text=='bag1':
                for bndbox in ob.iter('bndbox'):
                    for xmin in bndbox.iter('xmin'):
                        rect['xmin'] = xmin.text
                    for ymin in bndbox.iter('ymin'):
                        rect['ymin'] = ymin.text
                    for xmax in bndbox.iter('xmax'):
                        rect['xmax'] = xmax.text
                    for ymax in bndbox.iter('ymax'):
                        rect['ymax'] = ymax.text
                # draw
                cv2.rectangle(img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (0, 0, 255), 10)          
#            elif ob[0].text=='bag2':
#                for bndbox in ob.iter('bndbox'):
#                    for xmin in bndbox.iter('xmin'):
#                        rect['xmin'] = xmin.text
#                    for ymin in bndbox.iter('ymin'):
#                        rect['ymin'] = ymin.text
#                    for xmax in bndbox.iter('xmax'):
#                        rect['xmax'] = xmax.text
#                    for ymax in bndbox.iter('ymax'):
#                        rect['ymax'] = ymax.text
                # draw
                cv2.rectangle(img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (0, 255, 0), 10)                          
        
        cv2.imwrite(depth_dir.split('_')[0]+'_boundingbox.png',img)
