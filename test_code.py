# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:41:17 2019

@author: chaoz
"""

#Imports
import time
start = time.time()
import numpy as np
import os
import tensorflow as tf
from PIL import Image
import pandas as pd
 

  
os.chdir('./venv/models/research/object_detection/')
  
   
#Object detection imports
from object_detection.utils import label_map_util
 
 
from object_detection.utils import visualization_utils as vis_util
 
 
 
#Model preparation

MODEL_NAME = './venv/models/research/object_detection/models/model/model_fro_0325'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
 
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'bag.pbtxt')
 
NUM_CLASSES = 2
 
    
    
#Load a (frozen) Tensorflow model into memory.    
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')    
    
    
# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
 
 
# Helper code
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)
 
 
#Detection

# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = './venv/models/research/object_detection/data/test_sex_mix/'

 
# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)
 
#output_image_path = ("C:\\Users\\chaoz\\Desktop\\test_set_rgb")
# 另外加了输出识别结果框的坐标，保存为.csv表格文件
output_csv_path = ("./venv/models/research/object_detection/models/model/model_fro_0325/")

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    
    TEST_IMAGE_PATHS = PATH_TO_TEST_IMAGES_DIR

    data = pd.DataFrame()
    
    for image_path in os.listdir(TEST_IMAGE_PATHS):
      print(image_path)
      image = Image.open(PATH_TO_TEST_IMAGES_DIR+image_path)
      width, height = image.size
      # the array based representation of the image will be used later in order to prepare the
      # result image with boxes and labels on it.
      image_np = load_image_into_numpy_array(image)
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      image_np_expanded = np.expand_dims(image_np, axis=0)
      # Actual detection.
      (boxes, scores, classes, num) = sess.run(
          [detection_boxes, detection_scores, detection_classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # Visualization of the results of a detection.
      vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=8)
      #write images
      #保存识别结果图片
#%%      
#      rgb_f=image_path.split('_')[0]+'_RGB.png'
#      rgb_path='C:\\Users\\chaoz\\Desktop\\1121-3+2\\'+rgb_f
#      rgb_image = np.array(cv2.imread(rgb_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH))
#      vis_util.visualize_boxes_and_labels_on_image_array(
#          rgb_image,
#          np.squeeze(boxes),
#          np.squeeze(classes).astype(np.int32),
#          np.squeeze(scores),
#          category_index,
#          use_normalized_coordinates=True,
#          line_thickness=8,
#          max_boxes_to_draw=20,
#          min_score_thresh=.5)
#      cv2.imwrite(output_image_path+'\\'+image_path.split('\\')[-1],rgb_image)
      
      s_boxes = boxes[scores > 0.5]
      s_classes = classes[scores > 0.5]
      s_scores=scores[scores>0.5]
      
      #write table
      #保存位置坐标结果到 .csv表格
      for i in range(len(s_classes)):
          newdata= pd.DataFrame(0, index=range(1), columns=range(7))
          newdata.iloc[0,0] = image_path.split("\\")[-1].split('.')[0]
          newdata.iloc[0,1] = s_boxes[i][0]*height  #ymin
          newdata.iloc[0,2] = s_boxes[i][1]*width     #xmin
          newdata.iloc[0,3] = s_boxes[i][2]*height    #ymax
          newdata.iloc[0,4] = s_boxes[i][3]*width     #xmax
          newdata.iloc[0,5] = s_scores[i]
          newdata.iloc[0,6] = s_classes[i]

          data = data.append(newdata)
      data.to_csv(output_csv_path+'result.csv',index = False)
      
end =  time.time()
print("Execution Time: ", end - start)
