# Generation-dataset-personnalisé-pour-YOLOv7

Context

Cette année Formule ETS a pour projet de créer une voiture autonome. La compétition FSG Driverless est un événement annuel organisé par la Formula Student Germany (FSG), une compétition internationale de voitures de course étudiantes. L'objectif de la compétition Driverless est de concevoir, développer et construire des véhicules autonomes capables de naviguer et de concourir sur un circuit fermé constitué de cônes. Pour détecter les cônes, nous avons opté pour le modèle de reconnaissance d’objet YOLO V7 (You Only Look Once).Les données d’entrainement sont fournies au grand public sur le site fsOCO au format COCO(Common Objects in Context).

Objectif principal

Le projet consiste à développer un script permettant de convertir un dataset au format COCOpour entraîner le modèle YOLOV7 qui requiert un format diffèrent. Ce script convertit un dataset au format COCO en format YOLOV7, en effectuant plusieurs manipulations sur les images. L'objectif principal du programme est de fournir un dataset YOLO propre et présentable, tout en ajoutant des fonctionnalités souhaitées depuis un certain temps.

Prérequis

•	Python 3.6 ou version supérieure
•	OpenCV
•	PyYAML
•	tqdm
Assurez-vous d'installer les dépendances requises en utilisant la commande suivante : pip install -r requirements.txt

Utilisation

1.	Téléchargez le jeu de données brut "dataset_name" et placez-le dans le dossier approprié appelé datasets . Pour télécharger le dataset: http://fsoco.cs.uni-freiburg.de/src/download_boxes_train.php

2.	Exécutez le script "main.py" en utilisant les arguments suivants :

python .\main.py --dataset_name [NOM_DU_JEU_DE_DONNÉES] --output_name [NOM_DU_JEU_DE_DONNÉES_PRÉPARÉ] --train_count [TAUX_D'IMAGES_D'ENTRAÎNEMENT] --test_count [TAUX_D'IMAGES_DE_TEST] --image_count [NOMBRE_D'IMAGES_À_UTILISER] --blur_count [TAUX_D'IMAGES_FLUES]

•	dataset_name: Le nom du jeu de données brut à préparer.
•	output_name: Le nom du dossier de sortie où les données préparées seront enregistrées.
•	train_count: Le pourcentage d'images destinées à l'entraînement.
•	test_count: Le pourcentage d'images destinées aux tests.
•	image_count: Le nombre d'images à utiliser à partir du jeu de données brut. Si non fourni, toutes les images seront utilisées.
•	blur_count: Le pourcentage d'images avec effet de flou.

Structure du dossier de sortie

Le script générera la structure de dossiers suivante dans le dossier de sortie spécifié :
[NOM_DU_JEU_DE_DONNÉES_PRÉPARÉ]

    ├── train
    │   ├── images
    │   └── labels
    
    ├── test
    │   ├── images
    │   └── labels
    ├── val
    │   ├── images
    │   └── labels
    └── dataset.yaml
Les images transformées seront stockées dans les dossiers "images" correspondants, et les annotations associées seront enregistrées dans les dossiers "labels". Le fichier "dataset.yaml" sera également créé pour décrire la structure du jeu de données préparé.
