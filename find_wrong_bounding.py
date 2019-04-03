# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:00:25 2019

@author: chaoz
"""
import os

from PIL import Image
import cv2 as cv
import cv2
import numpy as np
import matplotlib.pyplot as plt


image_dir='C:\\Users\\chaoz\\Desktop\\save'

for dire in os.listdir(image_dir):
    RGB_dir=os.path.join(image_dir,dire)
    src = cv.imread(RGB_dir)
    cv2.namedWindow("enhanced",0);
    cv2.resizeWindow("enhanced", 800, 600);
    cv.imshow("enhanced",src)
    cv.waitKey(20)
    ws=input('请输入:')
    cv.destroyAllWindows()  
    if ws=='1':
        rgb_image = np.array(cv.imread(RGB_dir, cv.IMREAD_ANYCOLOR | cv.IMREAD_ANYDEPTH))
        print('move')
        cv.imwrite('C:\\Users\\chaoz\\Desktop\\move\\'+dire,rgb_image) 
    os.remove(RGB_dir)
        