import cv2
import numpy as np

def cut_inference(image_path, mask_path):
    im = cv2.imread(mask_path)
        
    x_min = 256
    y_min = 256
    x_max = 0
    y_max = 0
    xs = []
    ys = []
    
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i,j,0] == 255 and im[i,j,1] == 0 and im[i,j,2] == 0:
                xs.append(i)
                ys.append(j)
                
    poly = [(x + 0.5, y + 0.5) for x, y in zip(xs, ys)]            
    x_min = np.min(xs)
    y_min = np.min(ys)
    x_max = np.max(xs)
    y_max = np.max(ys)

    pts = np.array(poly, np.int32)
    im = cv2.imread(image_path)
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if cv2.pointPolygonTest(pts, [i,j], False) == -1.0:
                im[i,j] = 0
                    
    im = im[x_min:x_max, y_min:y_max]
        
    new_image = 'C:/Users/jorge/Desktop/AppResults/cut_' + image_path[-26:] 
    cv2.imwrite(new_image, im)
    
    return new_image