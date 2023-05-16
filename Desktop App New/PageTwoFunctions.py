# -*- coding: utf-8 -*-
"""
@author: JORGE PICADO CARINO
"""

import json
import numpy as np
import os, cv2

from PIL import ImageTk, Image
from tkinter import filedialog

import tkinter as tk  

dic_points = {}
  
# Opening JSON file
f = open(r"C:\Users\jorge\Desktop\all_via_region_data.json")
  
# returns JSON object as 
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for key, value in data.items():
    regions = value["regions"]
    filename = value["filename"]
    arch = filename[-26:]
    for it in regions:
      it = it["shape_attributes"]
      px = it["all_points_x"]
      py = it["all_points_y"]
      poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
      # poly = [p for x in poly for p in x]
      # poly = np.array(poly)

    dic_points[arch] = [poly]
  
# Closing file
f.close()


# route_image = r"C:\Users\jorge\Desktop\ALL_IMAGES_JSON\Dr7_587722981741363323.jpg"
# image_selected = route_image[-26:]

isClosed = True
 
# Blue color in BGR
color = (255, 0, 0)
 
# Line thickness of 1 px
thickness = 1

alpha = 0.4  # Transparency factor

def segment_image(image):
    if os.path.isfile(image):
        im = cv2.imread(image)
        
        image_selected = image[-26:]
        pts = np.array(dic_points[image_selected], np.int32)
        
        overlay = im.copy()
        cv2.fillPoly(overlay, [pts], (255, 207, 64))
        im = cv2.addWeighted(overlay, alpha, im, 1 - alpha, 0)
        
        im = cv2.polylines(im, [pts], isClosed, color, thickness)
        # cv2.imshow('Segmentation', im)
        
        cv2.waitKey(0)
        photo = fr"C:\Users\jorge\Desktop\outputs\SEG-{image.split('/')[-1].split('.')[0]}.png"
        cv2.imwrite(photo, im)
        
        return photo

def load_file(self):
    num_widgets = 0
    for widgets in self.winfo_children():
        # print(widgets)
        if(num_widgets > 3):
            widgets.destroy()
        
        num_widgets = num_widgets + 1
        
    global image_selected
    self.filename = filedialog.askopenfilename(initialdir=r"C:\Users\jorge\Desktop\ALL_IMAGES_JSON",
                                                 title="Select A File",
                                                 filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
    image_created = segment_image(self.filename)
    
    label = tk.Label(self, text=image_created)
    label.pack()
    
    image_selected = ImageTk.PhotoImage(Image.open(image_created))
    
    image_selected_label = tk.Label(self, image=image_selected)
    image_selected_label.pack()