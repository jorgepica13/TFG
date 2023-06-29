import torch
import seg_config_bin, seg_model, seg_utils

from PIL import Image

import cv2

def seg_inference(image_path):
    # Set computation device.
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    model = seg_model.prepare_model(len(seg_config_bin.ALL_CLASSES))
    ckpt = torch.load(r'C:\Users\jorge\Desktop\Models_files\best_model_seg.pth')
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval().to(device)
    
    # Read the image.
    image = Image.open(image_path)
    
    # Resize very large images (if width > 1024.) to avoid OOM on GPUs.
    if image.size[0] > 1024:
        image = image.resize((800, 800))
    
    # Do forward pass and get the output dictionary.
    outputs = seg_utils.get_segment_labels(image, model, device)
    # Get the data from the `out` key.
    outputs = outputs['out']
    segmented_image = seg_utils.draw_segmentation_map(outputs)
        
    final_image, final_mask = seg_utils.image_overlay(image, segmented_image)

    new_image = 'C:/Users/jorge/Desktop/AppResults/seg_' + image_path[-26:] 
    new_mask = 'C:/Users/jorge/Desktop/AppResults/mask_' + image_path[-26:-4] + '.png'
    cv2.imwrite(new_image, final_image)
    cv2.imwrite(new_mask, final_mask)
    
    return new_image, new_mask