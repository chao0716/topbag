# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:51:06 2019

@author: chaoz
"""

import xml.etree.ElementTree as ET
import cv2
import os

image_dir='C:\\Users\\chaoz\\Desktop\\(3+2)1123'
sname='RGB.png'
xmlname='xml'
RGB_dirlist=[]
xml_dirlist=[]
for dire in os.listdir(image_dir):
    pwd_dir=os.path.join(image_dir,dire)
    if sname in os.path.split(pwd_dir)[1]:
        RGB_dirlist.append(pwd_dir) 
    if xmlname in os.path.split(pwd_dir)[1]:
        xml_dirlist.append(pwd_dir)

for i in range(len(RGB_dirlist)):
    print(i,i/len(RGB_dirlist))
    RGB_dir=RGB_dirlist[i]
    xml_dir=RGB_dir.split('.')[0]+'.xml'
    if os.path.exists(xml_dir)==True:       
        tree = ET.parse(xml_dir)
        rect={}
        line=""
        root = tree.getroot()
        #image path in xml file
        for name in root.iter('path'):
            rect['path'] = name.text
        #open image before draw
        img=cv2.imread(RGB_dir)
        bag_count=0
        for ob in root.iter('object'):       
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
                if bag_count==0:
                    cv2.rectangle(img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (255, 0, 0), 3)          
                if bag_count==1:
                    cv2.rectangle(img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (0, 255, 0), 3)                 
                if bag_count==2:
                    cv2.rectangle(img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (0, 0, 255), 3)                 
                else:
                    cv2.rectangle(img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (255, 255, 255), 2)
                bag_count+=1
    
        
        cv2.imwrite(RGB_dir.split('.')[0]+'_boundingbox.png',img)
