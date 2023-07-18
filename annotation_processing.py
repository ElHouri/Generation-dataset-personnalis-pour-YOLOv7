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

from image_processing import crop_image, motion_blur

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(ROOT_DIR, "datasets")


DATASET_ANN_DIR = "ann"
DATASET_IMG_DIR = "img"

CATEGORIES = ["train", "test", "val"]

OUTPUT_IMG_DIR = "images"
OUTPUT_ANN_DIR = "labels"

fill_color = (0, 0, 0)

class_ids = {
    "unknown_cone": 0,
    "yellow_cone": 1,
    "blue_cone": 2,
    "orange_cone": 3,
    "large_orange_cone": 4,
    "knocked_over": 5
}
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------TRANSFORM ANNOTATION---------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#

def transform_annotation(data: dict, result_img) -> dict:
    
    objects = data["objects"]

    labels = []

    for object in objects:

        point1 = object["points"]["exterior"][0]
        point2 = object["points"]["exterior"][1]

        x = point1[0] - 140
        y = point1[1] - 140
        w = point2[0] - point1[0]
        h = point2[1] - point1[1]
        cone_title = object["classTitle"]
        cone_id = 0

        tags = [tag["name"] for tag in object["tags"]]

        if "knocked_over" in tags:
            cone_id = class_ids["knocked_over"]
        elif "sticker_band_removed" in tags or cone_title == "unknown_cone" or "issue: inaccurate bounding boxes" in tags or "issue: missing bounding boxes" in tags:
            cone_id = class_ids["unknown_cone"]
        else:
            cone_id = class_ids[cone_title]

        
        area=w*h
        if area < 500:
            cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 0, 0), -1)
            labels.append((x + int(w / 2), y + int(h / 2), w, h, cone_id))
    return result_img,labels


#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------PREPARE CATEGORY --------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#

def prepare_category(i_start, i_end, image_pairs, blur_percentage, category, output_dir):
    
    blur_count=int(blur_percentage*(i_end-i_start))
    
    for i in tqdm(range(i_start, i_end), desc=f"Image cropping {category}", colour="green", unit="img"):

        # Get the category (train, test, val) of the image
                
        name, image_file, annotation_file = image_pairs[i]
        #retourne une représentation sous forme de tableau multidimensionnel (NumPy array) de l'image.
        img = cv2.imread(image_file)
        if blur_count > 0:
            img =motion_blur(img, 13, i%2==0)
            blur_count -= 1

        result_img, result_size = crop_image(img, fill_color)
        
        # get json data from file
        json_data = None
        with open(annotation_file, 'r') as file:

            json_data = file.read()
            json_data = json.loads(json_data)
            

        result_img,labels = transform_annotation(json_data,result_img)
        
        
        cv2.imwrite(f"{output_dir}/{category}/{OUTPUT_IMG_DIR}/{name}.jpg", result_img)

        with open(f"{output_dir}/{category}/{OUTPUT_ANN_DIR}/{name}.txt", 'w') as text_file:
            for object in labels:
                
                x, y, w, h, class_id = object
                text_file.write(f"{class_id} {x/result_size} {y/result_size} {w/result_size} {h/result_size}\n")
