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

# from torchvision.models import alexnet, AlexNet_Weights
# from torchvision.models import vgg19_bn, VGG19_BN_Weights
# from torchvision.models import densenet201, DenseNet201_Weights
# from torchvision.models import efficientnet_b7, EfficientNet_B7_Weights
from torchvision.models import resnet50, ResNet50_Weights

# the computation device
device = ('cuda' if torch.cuda.is_available() else 'cpu')

# list containing all the class labels
labels = ['elliptical', 'spiral', 'uncertain']

# initialize the model and load the trained weights
# weights = AlexNet_Weights.DEFAULT
# model = alexnet(weights).to(device)

# weights = VGG19_BN_Weights.DEFAULT
# model = vgg19_bn(weights).to(device)

# weights = DenseNet201_Weights.DEFAULT
# model = densenet201(weights).to(device)

# weights = EfficientNet_B7_Weights.DEFAULT
# model = efficientnet_b7(weights).to(device)

weights = ResNet50_Weights.DEFAULT
model = resnet50(weights).to(device)

checkpoint = torch.load('/mnt/homeGPU/jpicado/TFG/classification/outputs_restored/model.pth', map_location=device)
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

def success_rate(image_test):
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

  if len(labels) <= int(output_label.indices):
    return -1

  pred_class = labels[int(output_label.indices)]

  if({gt_class} == {pred_class}):
    print(image_test[-26:])
    return 1
  return 0

ruta_dir = '/mnt/homeGPU/jpicado/TFG/dataset_restored/test'
contenido = os.listdir(ruta_dir)

total = 0
correct = 0
image_test = ''

for fichero in contenido:
  directory = os.path.join(ruta_dir, fichero)
  if os.path.isdir(directory):
    list_images = os.listdir(directory)

    for i in list_images:
      image_test = os.path.join(directory, i)
      if os.path.isfile(image_test) and i.endswith('.jpg'):
        if(success_rate(image_test) == 1):
          correct += 1
        
        total += 1

print('-----------------------------------------------------------')
print("El numero de aciertos ha sido: " + str(correct))
print("El numero de imagenes testeadas ha sido: " + str(total))

percentage = correct/total * 100
print("El porcentaje de acierto de test es de: " + str(percentage) + "%.")