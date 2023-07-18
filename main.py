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

from dataset import get_image_paths, get_profile, create_dataset_yaml, create_directories
from image_processing import crop_image, motion_blur
from annotation_processing import transform_annotation, prepare_category

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
#---------------------------------------------------------------MAIN-----------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#

def main(dataset_name: str, output_name: str, train: float, test: float, image_number: int, blur_count: float):
    
    FULL_DATASET_DIR = os.path.join(DATASET_DIR, dataset_name)
    
    #Create the complete path for the output directory by combining two variables
    output_dir: str = os.path.join(DATASET_DIR, output_name)
    #create the necessary directories for images and annotations (describing the images)
    create_directories(output_dir)
    #Create a YALM file
    create_dataset_yaml(output_dir)

    print(f"Retrieving files paths in: {FULL_DATASET_DIR}")
    print(f"Creating dataset with split repartition profile: {train},{test}")
    
    #Store the dataset directory, the paths of the corresponding images and annotation files
    image_pairs: list[tuple[str, str, str]] = get_image_paths(FULL_DATASET_DIR)
    
    # Get random image pairs if dataset as more image than specified image_number
    image_pairs = random.sample(image_pairs, min(len(image_pairs), image_number))
    random.shuffle(image_pairs)

    train_thres, test_thres = get_profile(train,test, len(image_pairs))
    
    #tqdm is a progress bar with the description "Image cropping" in green color.

    prepare_category(0, train_thres, image_pairs, blur_count, CATEGORIES[0], output_dir)
    prepare_category(train_thres, test_thres, image_pairs, blur_count, CATEGORIES[1], output_dir)
    prepare_category(test_thres, len(image_pairs), image_pairs, blur_count, CATEGORIES[2], output_dir)

    

#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------ARUGMENTS VERIFICATION---------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Parser for preparator params')
    
    #Name of the dataset file
    parser.add_argument('--dataset_name', type=str,
        help='name of the dataset file')
    
    #Name of the Output File
    parser.add_argument('--output_name', type=str,
        help='root path to output directory (will be created if not existing)')

    parser.add_argument('--train_count', type=float, default=1,
        help="""rate of train images""")
    
    parser.add_argument('--test_count', type=float, default=1,
        help="""rate of test images""")
    
    parser.add_argument('--image_count', type=int,
        help= "number of image to use from the input dataset, all images will be used if not provided"
    )
    parser.add_argument('--blur_count', type=float,
        help="""rate of blur images """)

    args = vars(parser.parse_args())
    
    if args['output_name'] != None and args['image_count'] != None:
        main(args['dataset_name'], args['output_name'],args['train_count'],args['test_count'], args['image_count'], args['blur_count'])
    else:
        print('Invalid arguments, --output_name and --image_count must be provided.' )
