# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 14:09:56 2019

@author: chaoz
"""

import xml.etree.ElementTree as ET
import cv2
import os
import numpy as np

import numpy  
my_matrix = numpy.loadtxt(open("test_set_rgb.csv","rb"),delimiter=",",skiprows=0,dtype=np.str)
for i in range(1,930):
    rgbdir='C:\\Users\\chaoz\\Desktop\\1121-3+2\\'+ my_matrix[i][0].split('_')[0]+'_RGB.png'
    xmin=int(float(my_matrix[i][1]))
    ymin=int(float(my_matrix[i][2]))
    xmax=int(float(my_matrix[i][3]))
    ymax=int(float(my_matrix[i][4]))
    bag_num=int(float(my_matrix[i][6]))
    if bag_num==1:
        rgb_image = np.array(cv2.imread(rgbdir, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))
        cv2.resize(rgb_image, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        cv2.rectangle(rgb_image, (ymin,xmin),(ymax,xmax), (0, 255, 0), 10) 
    cv2.imwrite(rgbdir.split('_')[0]+'_result.png',rgb_image)
        
