# image_processing.py
#This class will handle image processing and manipulation.

import cv2
import yaml
import os
from fnmatch import fnmatch
from tqdm import tqdm
import json
import numpy as np
import random
import argparse
import shutil
import math



#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------CROP IMAGE----------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
     
            
def crop_image(img: np.ndarray, fill_color):
# Retrieve the height of the image
    height = img.shape[0]
# Retrieve the width of the image
    width = img.shape[1]
# Retrieve the number of channels of the image
    channels = img.shape[2]
#Cropping by subtracting 280 pixels from the original height and width. 
    post_cropp_height = height - 280
    post_cropp_width = width - 280

    result_size = max(post_cropp_height, post_cropp_width)
    result_img = np.full((result_size, result_size, channels), fill_color, dtype=np.uint8)
    
    img = img[140:height - 140, 140:width - 140]
    result_img[0:post_cropp_height, 0:post_cropp_width] = img
    return result_img, result_size
    
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------------MOTION BLUR----------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
def motion_blur(image, kernel_size: int, isVertical: bool):
     # Create the motion blur kernel    
    kernel_v = np.zeros((kernel_size, kernel_size))
    # Calculate the center coordinates of the kernel
    kernel_h = np.copy(kernel_v)
    # Fill the middle row with ones.
    if isVertical:
        kernel_v[:, int((kernel_size - 1)/2)] = np.ones(kernel_size)
        # Normalize.
        kernel_v /= kernel_size
        # Apply the vertical kernel.
        return cv2.filter2D(image, -1, kernel_v)
    else : 
        kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
        # Normalize.
        kernel_h /= kernel_size
        # Apply the horizontal kernel.
        return cv2.filter2D(image, -1, kernel_h)
