# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 12:25:11 2019

@author: chaoz
"""

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


#image_dir='C:\\Users\\chaoz\\Desktop\\trainset\\'
#xml_floder='C:\\Users\\chaoz\\Desktop\\trainxml\\'
image_dir='C:\\Users\\chaoz\\Desktop\\testset\\'
xml_floder='C:\\Users\\chaoz\\Desktop\\testxml\\'
csv_save_dir=''
sname='RGB.png'
xmlname='xml'
RGB_dirlist=[]
xml_dirlist=[]
for dire in os.listdir(image_dir):
    if sname in os.path.split(dire)[1]:
        RGB_dirlist.append(dire) 

xml_list = []
for i in range(len(RGB_dirlist)):
    RGB_dir=image_dir+RGB_dirlist[i]
    xml_dir=xml_floder+RGB_dirlist[i].split('_')[0]+'_RGB.xml'
    if os.path.exists(xml_dir)==True:  
        print(i,i/len(RGB_dirlist))
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        for member in root.findall('object'):
            if member[0].text=='bag1':
                value = (root.find('filename').text.split('_')[0]+'_mix.png',
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text),
                         member[0].text,
                         int(member[4][0].text),
                         int(member[4][1].text),
                         int(member[4][2].text),
                         int(member[4][3].text)
                         )
                xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)


xml_df.to_csv(csv_save_dir+'mix_test.csv', index=None)
print('Successfully converted xml to csv.')
