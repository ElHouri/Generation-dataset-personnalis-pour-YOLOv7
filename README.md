# Generation-dataset-personnalis-pour-YOLOv7
1-Context
Cette ann´ee Formule ETS a pour projet de cr´eer une voiture autonome. La comp´etition FSG Driverless est un ´ev´enement
annuel organis´e par la Formula Student Germany (FSG), une comp´etition internationale de voitures de course ´etudiantes.
L’objectif de la comp´etition Driverless est de concevoir, d´evelopper et construire des v´ehicules autonomes capables de
naviguer et de concourir sur un circuit ferm´e constitu´e de cˆones. Pour d´etecter les cˆones, nous avons opt´e pour le mod`ele d
e reconnaissance d’objet YOLO V7 (You Only Look Once).Les donn´ees d’entrainement sont fournies au grand public sur le
site fsOCO au format COCO(Common Objects in Context).
2-Objectif principal
Le projet consiste `a d´evelopper un script permettant de convertir un dataset au format COCOpour entraˆıner le mod`ele
YOLOV7 qui requiert un format diff`erent. Ce script convertit un dataset au format COCO en format YOLOV7, en
effectuant plusieurs manipulations sur les images. L’objectif principal du programme est de fournir un dataset YOLO
propre et pr´esentable, tout en ajoutant des fonctionnalit´es souhait´ees depuis un certain temps
3-Prérequis
Python 3.6 ou version supérieure
OpenCV
PyYAML
tqdm
Assurez-vous d'installer les dépendances requises en utilisant la commande suivante :
•	pip install -r requirements.txt
