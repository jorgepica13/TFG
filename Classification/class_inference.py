import sys, os
# change directory
# %cd '/mnt/homeGPU/jpicado/TFG/classification/'
# Let's import the python files to have access to its functions and Classes
path_to_module='/mnt/homeGPU/jpicado/TFG/classification/'
sys.path.append(os.path.abspath(path_to_module))
import class_utils, class_model, class_datasets

import torch
import cv2
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
import torch.nn.functional as F

# the computation device
device = ('cuda' if torch.cuda.is_available() else 'cpu')

# list containing all the class labels
labels = ['elliptical', 'spiral', 'uncertain']

# initialize the model and load the trained weights
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights).to(device)

checkpoint = torch.load('/mnt/homeGPU/jpicado/TFG/classification/outputs_ResNet/model.pth', map_location=device)
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

image_test = '/mnt/homeGPU/jpicado/TFG/dataset_or/test/elliptical/Dr7_587725469590749389.jpg'

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
    outputs = model(image.to(device))
output_label = torch.topk(outputs, 1)

probs = F.softmax(outputs, dim=1)
probs3 = probs.topk(3)
# Valor de confianza en la prediccion de la clase
confidence_value = '{:.2f}'.format(float(probs3.values[0,0])*100)

pred_class = labels[int(output_label.indices)]

print(f"GT: {gt_class}, pred: {pred_class}")
print('Porcentaje de confianza: ', confidence_value, '%')