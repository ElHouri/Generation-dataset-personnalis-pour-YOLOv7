# dataset_utils.py
#this module will contain functions related to handling datasets and image paths.
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
#-----------------------------------------ARUGMENTS VERIFICATION---------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#eturns a list of tuples containing information about the image paths and annotation path      
def get_image_paths(FULL_DATASET_DIR) -> list[tuple[str, str, str]]:
    
    # Image name, Image path, annotation path
    image_pairs: list[tuple[str, str, str]] = []
    
    # List all subdirectories, but not the files
    # team_folders = [f for f in os.listdir(FULL_DATASET_DIR) if os.path.isdir(os.path.join(FULL_DATASET_DIR, f))]
    team_folders = []
    found_items = os.listdir(FULL_DATASET_DIR)
    for item in found_items:
        if os.path.isdir(os.path.join(FULL_DATASET_DIR, item)):
            team_folders.append(item)
    
    for team_folder in team_folders:
        
        ann_dir = os.path.join(FULL_DATASET_DIR, team_folder, DATASET_ANN_DIR)
        img_dir = os.path.join(FULL_DATASET_DIR, team_folder, DATASET_IMG_DIR)
        
        # Make sure both image and annotation folders exist
        if not os.path.exists(ann_dir) or not os.path.exists(img_dir):
            print(f"Skipping {team_folder} as it does not contain both an image and annotation folder")
            continue
        
        # Get all annotations (json files) in the annotation folder
        annotations=[]
        for file in os.listdir(ann_dir):
            if os.path.isfile(os.path.join(ann_dir, file)) and fnmatch(file, "*.json"):
                annotations.append(file)
       
        
        # Get all images (jpg and png files) in the image folder
    
        images=[]
        for file in os.listdir(img_dir):
            if os.path.isfile(os.path.join(img_dir, file)) and (fnmatch(file, "*.jpg") or fnmatch(file, "*.png")):
                images.append(file)
                
        # Validate that every image has an annotation, filter out the ones that don't
        validated_images=[]
        for image in images:
            annotation_file = f"{image}.json"
            if annotation_file in annotations:
                validated_images.append(image)

        
        # Get the full path for each image and annotations
        for image in validated_images:
            image_path = os.path.join(img_dir, image)
            anno_path = os.path.join(ann_dir, f"{image}.json")
            
            # Remove file extensions
            name = os.path.splitext(image)[0]
            
            image_pairs.append((name, image_path, anno_path))
        
    return image_pairs
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------GET PROFILE--------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#

def get_profile(profile_train: int, profile_test: int, image_count: int) -> tuple[int, int]:
    
    #Rate of validation image 
    profile_val=1-(profile_train+profile_test)
        
    # Make sure the profile is valid, (total == 1)
    total = profile_train+profile_test+profile_val
        
    if (abs(1 - total)) > 0.0001:
        print(f"Invalid split profile because the total: {total} is different from 1")
        exit(1)
        
    # Number of trainning images
    train = int(image_count * profile_train)
    # Number of testing images
    test = train + int(image_count *profile_test)
    
    return (train, test)
   
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------CREATION DATA SET YAML FILE----------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#Used to convert Python data into the YAML format and write it to a specified YAML file.

def create_dataset_yaml(output_dir: str):
    
    with open(f"{output_dir}/dataset.yaml", 'w') as yamlfile:
    #Create a dictionnary
        content = {
            "train": f"{output_dir}/train/images",
            "test": f"{output_dir}/test/images",
            "val": f"{output_dir}/val/images",
            "nc": len(class_ids),
            "names": list(class_ids.keys())
        }
        #Convert Python data into the YAML format
        yaml.dump(content, yamlfile)
       
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------CREATION DIRECTORIES-----------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#    
#create the necessary directories for storing the output images and annotation files in the desired output structure.

def create_directories(output_dir: str):
    
    for category in CATEGORIES:
        IMG_DIR=f"{output_dir}/{category}/{OUTPUT_IMG_DIR}"
        ANN_DIR=f"{output_dir}/{category}/{OUTPUT_ANN_DIR}"
        
        if os.path.exists(IMG_DIR):
            choice = input(f"The directory {category} '{OUTPUT_IMG_DIR}' already exists. Do you want to delete it? (y/n): ")
            if choice.lower() == 'y':
                shutil.rmtree(IMG_DIR)
            else :
                continue 
        if os.path.exists(ANN_DIR):
            choice = input(f"The directory {category} '{OUTPUT_ANN_DIR}' already exists. Do you want to delete it? (y/n): ")
            if choice.lower() == 'y':
                shutil.rmtree(ANN_DIR)
            else :
                continue 
                
        os.makedirs(IMG_DIR)
        os.makedirs(ANN_DIR)    
