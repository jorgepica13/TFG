# -*- coding: utf-8 -*-
"""
@author: JORGE PICADO CARINO
"""

import torch
import torchvision.transforms as transforms
import numpy as np
import cv2

# from model import CNNMOdel
from torchvision.models import resnet50, ResNet50_Weights

def credibility(output_labels):
  values = [0, 0, 0]
  
  nlabels = len(output_labels.indices[0])
  for i in range(nlabels):
    values[int(output_labels.indices[0,i])] = float(output_labels.values[0,i])

  total = np.sum(values)
  max = np.max(values)

  return float(max/total * 100)


def class_inference(image_test):
    # the computation device
    device = ('cuda' if torch.cuda.is_available() else 'cpu')
    
    # list containing all the class labels
    labels = ['elliptical', 'spiral', 'uncertain']
    
    # initialize the model and load the trained weights
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights).to(device)
    
    checkpoint = torch.load(r'C:\Users\jorge\Desktop\Models_files\class_model.pth', map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
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
    #gt_class = image_test.split('/')[-2]
    # orig_image = image.copy()
    # convert to RGB format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = transform(image)
    # add batch dimension
    image = torch.unsqueeze(image, 0)
    with torch.no_grad():
        outputs = model(image.to(device))
    output_label = torch.topk(outputs, 1)
    
    # Valor de confianza en la prediccion de la clase
    confidence_value = credibility(torch.topk(outputs, 3))
    
    pred_class = labels[int(output_label.indices)]
    '''
    cv2.putText(orig_image, 
        f"GT: {gt_class}",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.6, (0, 255, 0), 2, cv2.LINE_AA
    )
    cv2.putText(orig_image, 
        f"Pred: {pred_class}",
        (10, 55),
        cv2.FONT_HERSHEY_SIMPLEX, 
        0.6, (0, 0, 255), 2, cv2.LINE_AA
    )
    
    print(f"GT: {gt_class}, pred: {pred_class}")
    print('Porcentaje de confianza: ', confidence_value, '%')
    cv2.imshow(orig_image)
    cv2.waitKey(0)
    cv2.imwrite(f"outputs/{gt_class}{image_test.split('/')[-1].split('.')[0]}.png", orig_image)
    '''
    
    return pred_class, confidence_value