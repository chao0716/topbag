# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 13:21:04 2019

@author: chaoz
"""


import xml.etree.ElementTree as ET
import cv2
import os
import numpy as np

image_dir='C:\\Users\\chaoz\\Desktop\\(3+2)1123\\'
save_dir='C:\\Users\\chaoz\\Desktop\\save\\'
my_matrix = np.loadtxt(open("0401_train_15000_result.csv","rb"),delimiter=",",skiprows=0,dtype=np.str)
my_matrix = np.delete(my_matrix,0,axis=0)

name_list=[]
x_list=[]
y_list=[]
prob_list=[]
class_list=[]
xmin_list=[]
ymin_list=[]
xmax_list=[]
ymax_list=[]
for i in range(len(my_matrix)):
    name_list.append(my_matrix[i][0])
    ymin_list.append(float(my_matrix[i][1]))
    xmin_list.append(float(my_matrix[i][2]))
    ymax_list.append(float(my_matrix[i][3]))
    xmax_list.append(float(my_matrix[i][4]))
    x_list.append((float(my_matrix[i][3])-float(my_matrix[i][1]))/2+float(my_matrix[i][1]))
    y_list.append((float(my_matrix[i][4])-float(my_matrix[i][2]))/2+float(my_matrix[i][2]))
    prob_list.append(float(my_matrix[i][5]))
    class_list.append(int(float(my_matrix[i][6])))

#for i in range(len(name_list)):
#    if name_list[i]=='2018-11-20-10-08-55_mix':
#        print(i)
#    rgb_img_dir=image_dir+name_list[i]+'.png'
#    xml_dir=image_dir+name_list[i].split('_')[0]+'_RGB.xml'
#    rgb_img = cv2.imread(rgb_img_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
#    if int(class_list[i])==1:
#        cv2.circle(rgb_img, (int(y_list[i]),int(x_list[i])), 50, (0,255,255), -10)
#        cv2.rectangle(rgb_img, (int(xmin_list[i]), int(ymax_list[i])), (int(xmax_list[i]), int(ymin_list[i])), (0, 255, 255), 3)
#        cv2.putText(rgb_img,str(round(prob_list[i], 3)),(int(xmin_list[i])+30, int(ymax_list[i])+30),cv2.FONT_HERSHEY_PLAIN,2.0,(255,0,255),3)
#    #draw boundingbox
#    tree = ET.parse(xml_dir)
#    rect={}
#    line=""
#    root = tree.getroot()
#    for ob in root.iter('object'): 
#        if ob[0].text=='bag1':
#            for bndbox in ob.iter('bndbox'):
#                for xmin in bndbox.iter('xmin'):
#                    rect['xmin'] = xmin.text
#                for ymin in bndbox.iter('ymin'):
#                    rect['ymin'] = ymin.text
#                for xmax in bndbox.iter('xmax'):
#                    rect['xmax'] = xmax.text
#                for ymax in bndbox.iter('ymax'):
#                    rect['ymax'] = ymax.text
#            # draw
#            cv2.rectangle(rgb_img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (0, 255, 0), 5)          
#    cv2.imwrite(rgb_img_dir,rgb_img)    

need_d=[]         
for i in range(len(my_matrix)):
    if int(class_list[i])==2:
        need_d.append(i)
name_list=np.array(name_list, dtype = str) 
x_list=np.array(x_list, dtype = float) 
y_list=np.array(y_list, dtype = float) 
prob_list=np.array(prob_list, dtype = float) 
need_d=np.array(need_d, dtype = int)
xmin_list=np.array(xmin_list, dtype = float)
ymin_list=np.array(ymin_list, dtype = float)
xmax_list=np.array(xmax_list, dtype = float)
ymax_list=np.array(ymax_list, dtype = float)                   
  
name_list = np.delete(name_list,need_d,axis=0)
prob_list = np.delete(prob_list,need_d,axis=0)  
x_list = np.delete(x_list,need_d,axis=0)  
y_list = np.delete(y_list,need_d,axis=0)
xmin_list = np.delete(xmin_list,need_d,axis=0)
ymin_list = np.delete(ymin_list,need_d,axis=0)
xmax_list = np.delete(xmax_list,need_d,axis=0)
ymax_list = np.delete(ymax_list,need_d,axis=0)

for j in range(2000):            
    for i in range(len(name_list)):
        if i+1==len(name_list):
            break
        else:
            cur_name=name_list[i]
            next_name=name_list[i+1]  
        if cur_name==next_name:
            if prob_list[i]>prob_list[i+1]:
                name_list = np.delete(name_list,i+1,axis=0)
                prob_list = np.delete(prob_list,i+1,axis=0)  
                x_list = np.delete(x_list,i+1,axis=0)  
                y_list = np.delete(y_list,i+1,axis=0)
                xmin_list = np.delete(xmin_list,i+1,axis=0)
                ymin_list = np.delete(ymin_list,i+1,axis=0)
                xmax_list = np.delete(xmax_list,i+1,axis=0)
                ymax_list = np.delete(ymax_list,i+1,axis=0)
                break
            elif prob_list[i]<=prob_list[i+1]:
                name_list = np.delete(name_list,i,axis=0)
                prob_list = np.delete(prob_list,i,axis=0)  
                x_list = np.delete(x_list,i,axis=0)  
                y_list = np.delete(y_list,i,axis=0)
                xmin_list = np.delete(xmin_list,i+1,axis=0)
                ymin_list = np.delete(ymin_list,i+1,axis=0)
                xmax_list = np.delete(xmax_list,i+1,axis=0)
                ymax_list = np.delete(ymax_list,i+1,axis=0)
                break
success=0
for i in range(len(name_list)):
    xml_dir=image_dir+name_list[i].split('_')[0]+'_RGB.xml'
    tree = ET.parse(xml_dir)
    rect={}
    line=""
    root = tree.getroot()
    sec_count=0
    rgb_img_dir=image_dir+name_list[i].split('_')[0]+'_RGB.png'
    rgb_img = cv2.imread(rgb_img_dir,cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    cv2.rectangle(rgb_img, (int(xmin_list[i]), int(ymax_list[i])), (int(xmax_list[i]), int(ymin_list[i])), (255, 0, 0), 2)
    cv2.putText(rgb_img,str(round(prob_list[i], 3)),(int(xmin_list[i])+30, int(ymax_list[i])+30),cv2.FONT_HERSHEY_PLAIN,2.0,(255,0,255),3)
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
            cv2.rectangle(rgb_img, (int(rect['xmin']), int(rect['ymax'])), (int(rect['xmax']), int(rect['ymin'])), (0, 255, 0), 2) 
            cv2.putText(rgb_img,'Ground_truth',(int(xmin_list[i])+30, int(ymax_list[i])+30),cv2.FONT_HERSHEY_PLAIN,2.0,(0,255,0),10)             
    cv2.imwrite('C:\\Users\\chaoz\\Desktop\\save\\'+name_list[i].split('_')[0]+'_RGB.png',rgb_img) 
