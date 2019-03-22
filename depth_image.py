# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 15:20:46 2019

@author: chaoz
"""

import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET

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
    depth_image_path=depth_dir
    depth_image = np.array(cv2.imread(depth_image_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))
    
    im=depth_image.astype(int)
    #im=im[50:800,200:1080]
    min_exclude_0=im[im!=0].min()
    max_exclude_0=im[im!=0].max()
    
    diff = max_exclude_0 - min_exclude_0
    
    
    for i in range (np.shape(im)[0]):
        for j in range(np.shape(im)[1]):
            if im[i,j]!=0:
                im[i,j]=(im[i,j]-min_exclude_0)*255/diff
    
    mean_list=[]
    var_list=[]
    x_list=[]
    y_list=[]
    w_size=200
    im[np.where(im==0)]=255
#    for i in range(np.shape(im)[0]-w_size):
#        for j in range(np.shape(im)[1]-w_size):
#            part_im=im[i:i+w_size,j:j+w_size]
#            mean_list.append(part_im.mean())
#            var_list.append(part_im.var())
#            y_list.append(i)
#            x_list.append(j)
            
    for i in range(int((np.shape(im)[0]-w_size)/10)):
        for j in range(int((np.shape(im)[1]-w_size)/10)):
            
            part_im=im[i*10:i*10+w_size,j*10:j*10+w_size]
            mean_list.append(part_im.mean())
            var_list.append(part_im.var())
            y_list.append(i*10)
            x_list.append(j*10)
    
    mean_list.index(min(mean_list))        
    top_x= x_list[mean_list.index(min(mean_list))]+(w_size/2)
    top_y= y_list[mean_list.index(min(mean_list))]+(w_size/2)

    bag1_xmin=[]
    bag1_ymin=[]
    bag1_xmax=[]
    bag1_ymax=[]
    bag1_count=0
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
    success=0            
    for i in range(bag1_count):
        if top_x > bag1_xmin[i] and top_x < bag1_xmax[i] and top_y > bag1_ymin[i] and top_y < bag1_ymax[i]:
            success+=1
    if success>0:
        total_sc+=1
    print('total_sc', total_sc)    
                     



















#my_matrix = np.loadtxt(open("train.csv","rb"),delimiter=",",skiprows=0,dtype=bytes).astype(str)
#
#my_matrix = np.delete(my_matrix, [1,2], axis=1)
#my_matrix = np.delete(my_matrix, 0, axis=0)

depth_image_path=''
depth_image = np.array(cv2.imread(depth_image_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))

im=depth_image.astype(int)
#im=im[50:800,200:1080]
min_exclude_0=im[im!=0].min()
max_exclude_0=im[im!=0].max()

diff = max_exclude_0 - min_exclude_0


for i in range (np.shape(im)[0]):
    for j in range(np.shape(im)[1]):
        if im[i,j]!=0:
            im[i,j]=(im[i,j]-min_exclude_0)*255/diff

mean_list=[]
var_list=[]
x_list=[]
y_list=[]
w_size=200
im[np.where(im==0)]=255
for i in range(np.shape(im)[0]-w_size):
    print(i)
    for j in range(np.shape(im)[1]-w_size):
        part_im=im[i:i+w_size,j:j+w_size]
        mean_list.append(part_im.mean())
        var_list.append(part_im.var())
        y_list.append(i)
        x_list.append(j)

mean_list.index(min(mean_list))        
print('x:', x_list[mean_list.index(min(mean_list))]+125)
print('y:', y_list[mean_list.index(min(mean_list))]+125)


#image_dir='C:\\Users\\chaoz\\Desktop\\(3+2)1123'
#sname='RGB.png'
#RGB_dirlist=[]
#for dire in os.listdir(image_dir):
#    pwd_dir=os.path.join(image_dir,dire)
#    if sname in os.path.split(pwd_dir)[1]:
#        RGB_dirlist.append(pwd_dir) 
