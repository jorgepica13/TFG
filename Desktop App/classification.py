import torch
import torchvision.transforms as transforms
import cv2
import torch.nn.functional as F

from torchvision.models import resnet50, ResNet50_Weights

def class_inference(image_test):
    # the computation device
    device = ('cuda' if torch.cuda.is_available() else 'cpu')
    
    # list containing all the class labels
    labels = ['elliptical', 'spiral', 'uncertain']
    
    # initialize the model and load the trained weights
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights).to(device)
    
    checkpoint = torch.load(r'C:\Users\jorge\Desktop\Models_files\best_model_class.pth', map_location=device)
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
    
    return pred_class, confidence_value