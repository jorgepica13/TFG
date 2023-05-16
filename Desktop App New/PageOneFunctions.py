# -*- coding: utf-8 -*-
"""
@author: JORGE PICADO CARINO
"""

import torch
import cv2
import torchvision.transforms as transforms

import sys
sys.path.append(r'C:\Users\jorge\Desktop\Training CNN Model')
import utils, model, datasets

from PIL import ImageTk, Image
from tkinter import filedialog

import tkinter as tk  

def classify_image(image_test):
    # the computation device
    device = ('cuda' if torch.cuda.is_available() else 'cpu')
    
    # list containing all the class labels
    labels = ['elliptical', 'spiral', 'uncertain']
    
    # initialize the model and load the trained weights
    modelo = model.CNNModel().to(device)
    checkpoint = torch.load(r'C:\Users\jorge\Desktop\outputs\model.pth', map_location=device)
    modelo.load_state_dict(checkpoint['model_state_dict'])
    modelo.eval()
    
    # define preprocess transforms
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.5, 0.5, 0.5],
            std=[0.5, 0.5, 0.5]
        )
    ])
    
    # read and preprocess the image
    image = cv2.imread(image_test)
    # get the ground truth class
    gt_class = image_test.split('/')[-2]
    orig_image = image.copy()
    # convert to RGB format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = transform(image)
    # add batch dimension
    image = torch.unsqueeze(image, 0)
    with torch.no_grad():
        outputs = modelo(image.to(device))
    output_label = torch.topk(outputs, 1)
    pred_class = labels[int(output_label.indices)]
    cv2.putText(orig_image, 
        f"GT: {gt_class}",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.6, (0, 255, 0), 2, cv2.LINE_AA
    )
    
    color_pred = (0, 0, 255)
    if({gt_class} == {pred_class}):
        color_pred = (255, 0, 0)
        
    cv2.putText(orig_image, 
        f"Pred: {pred_class}",
        (10, 55),
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.6, color_pred, 2, cv2.LINE_AA
    )
    
    print(f"GT: {gt_class}, pred: {pred_class}")
    # cv2.imshow('Result: ', orig_image)
    cv2.waitKey(0)
    photo = fr"C:\Users\jorge\Desktop\outputs\{gt_class}-{image_test.split('/')[-1].split('.')[0]}.png"
    cv2.imwrite(photo, orig_image)

    return photo