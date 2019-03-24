# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:45:16 2019

@author: chaoz
"""

import xml.etree.ElementTree as ET
import cv2
import os
import numpy as np

image_dir='C:\\Users\\chaoz\\Desktop\\1121-3+2\\'
save_dir='C:\\Users\\chaoz\\Desktop\\save\\'
my_matrix = np.loadtxt(open("ouy.csv","rb"),delimiter=",",skiprows=0,dtype=np.str)
my_matrix = np.delete(my_matrix,0,axis=0)

name_list=[]
x_list=[]
y_list=[]
prob_list=[]
class_list=[]

for i in range(len(my_matrix)):
    name_list.append(my_matrix[i][0])
    x_list.append((float(my_matrix[i][3])-float(my_matrix[i][1]))/2+float(my_matrix[i][1]))
    y_list.append((float(my_matrix[i][4])-float(my_matrix[i][2]))/2+float(my_matrix[i][2]))
    prob_list.append(float(my_matrix[i][5]))
    class_list.append(int(float(my_matrix[i][6])))

for i in range(len(name_list)):
    rgb_img_dir=image_dir+name_list[i]+'.png'
    xml_dir=image_dir+name_list[i]+'.xml'
    rgb_img = cv2.imread(rgb_img_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    if int(class_list[i])==1:
        cv2.circle(rgb_img, (int(x_list[i]),int(y_list[i])), 10, (0,255,255), -10)
    
    #draw boundingbox
    tree = ET.parse(xml_dir)
    rect={}
    line=""
    root = tree.getroot()
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
            cv2.rectangle(rgb_img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (0, 0, 255), 10)          
    cv2.imwrite(save_dir+name_list[i]+'_boundingbox.png',rgb_img)

need_d=[]         
for i in range(len(my_matrix)):
    if int(class_list[i])==2:
        need_d.append(i)
name_list=np.array(name_list, dtype = str) 
x_list=np.array(x_list, dtype = float) 
y_list=np.array(y_list, dtype = float) 
prob_list=np.array(prob_list, dtype = float) 
need_d=np.array(need_d, dtype = int)                   
  
name_list = np.delete(name_list,need_d,axis=0)
prob_list = np.delete(prob_list,need_d,axis=0)  
x_list = np.delete(x_list,need_d,axis=0)  
y_list = np.delete(y_list,need_d,axis=0)

for j in range(1000):            
    for i in range(len(name_list)):
        cur_name=name_list[i]
        next_name=name_list[i+1]  
        if i+2==len(name_list):
            break
        if cur_name==next_name:
            if prob_list[i]>prob_list[i+1]:
                name_list = np.delete(name_list,i+1,axis=0)
                prob_list = np.delete(prob_list,i+1,axis=0)  
                x_list = np.delete(x_list,i+1,axis=0)  
                y_list = np.delete(y_list,i+1,axis=0)
                break
            elif prob_list[i]<=prob_list[i+1]:
                name_list = np.delete(name_list,i,axis=0)
                prob_list = np.delete(prob_list,i,axis=0)  
                x_list = np.delete(x_list,i,axis=0)  
                y_list = np.delete(y_list,i,axis=0)
                break
success=0
for i in range(len(name_list)):
    xml_dir=image_dir+name_list[i]+'.xml'
    tree = ET.parse(xml_dir)
    rect={}
    line=""
    root = tree.getroot()
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
    if int(rect['xmax'])<x_list[i]<int(rect['xmax']) and  int(rect['ymax'])<y_list[i]<int(rect['ymax']):
        success+=1
print(success,len(name_list),success/len(name_list))    
          
            
            