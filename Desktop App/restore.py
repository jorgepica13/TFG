from RealESRGAN import RealESRGAN
from PIL import Image
import numpy as np
import torch
import cv2

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# print('device:', device)

model_scale = "4" #@param ["2", "4", "8"] {allow-input: false}

model = RealESRGAN(device, scale=int(model_scale))
model.load_weights(f'weights/RealESRGAN_x{model_scale}.pth')

# Upload and upscale images or .tar archives
def process_input(filename):
    res_name = 'C:/Users/jorge/Desktop/AppResults/res_' + filename[-26:]
    
    image = Image.open(filename).convert('RGB')
    sr_image = model.predict(np.array(image))
    sr_image.save(filename)

    img_output = cv2.imread(filename)
    cv2.imwrite(res_name, img_output)
    
    return res_name