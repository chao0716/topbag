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

only1=0
kdanfkn=0
total_sc=0
image_dir='C:\\Users\\chaoz\\Desktop\\(3+2)1123'
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
    print(de)
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
        
        im=depth_image.astype(int)
        min_exclude_0=im[im!=0].min()
        max_exclude_0=im[im!=0].max()
        
        diff = max_exclude_0 - min_exclude_0
        
        
        for i in range (np.shape(im)[0]):
            for j in range(np.shape(im)[1]):
                if im[i,j]!=0:
                    im[i,j]=(im[i,j]-min_exclude_0)*255/diff
        
        bag1_mean_list=[]
        bag1_var_list=[]
        im[np.where(im==0)]=255
        for i in range(bag1_count):
            k=i
            part_im=im[bag1_ymin[k]+100:bag1_ymax[k]-100,bag1_xmin[k]+50:bag1_xmax[k]-50]
            bag1_mean_list.append(part_im.mean())
            bag1_var_list.append(part_im.var())
            
        bag2_mean_list=[]
        bag2_var_list=[]
        for i in range(bag2_count):
            k2=i
            part_im=im[bag2_ymin[k2]:bag2_ymax[k2],bag2_xmin[k2]:bag2_xmax[k2]]
            bag2_mean_list.append(part_im.mean())
            bag2_var_list.append(part_im.var())
        
        if bag2_mean_list: 
            kdanfkn+=1
            if min(bag1_mean_list)<min(bag2_mean_list):
                total_sc+=1
                print(total_sc/kdanfkn)
            else:
                print(RGB_dir)
        else:
            only1+=1
            
print(only1,total_sc,kdanfkn) 
 
                     