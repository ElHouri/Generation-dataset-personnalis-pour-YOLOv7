Cas de test - Exemple d'exécution du programme

Pour illustrer l'exécution du programme, nous allons utiliser la documentation officielle de YOLO pour comprendre le format d'annotation YOLO.

Pour récupérer des fichiers au format COCO, on utilise le lien https://www.fsoco-dataset.com/ pour avoir accès à une banque de données accessible au grand publique.

Le fichier téléchargé qui contient des images et des annotations brutes. 

Nous allons préparer ce jeu de données pour l'entraînement de YoloV7 modèle de détection d'objets et enregistrer les données préparées dans un nouveau dossier nommé "output".

Étape 1: Téléchargement du jeu de données brut
Téléchargez le jeu de données brut "dataset_name" et placez-le dans le dossier approprié . 
Pour télécharger le dataset: http://fsoco.cs.uni-freiburg.de/src/download_boxes_train.php


Étape 2: Exécution du script
Ouvrez un terminal et exécutez le script "main.py" avec les arguments appropriés :

python .\main.py --dataset_name fsoco_bounding_boxes_train --output_name output --train_count 0.3 --test_count 0.5  --image_count 200 --blur_count 0.5

Explication des arguments utilisés :
--dataset_name fsoco_bounding_boxes_train: Le nom du jeu de données brut à préparer.
--output_name output: Le nom du dossier de sortie où les données préparées seront enregistrées.
--train_count 0.3: Le pourcentage d'images destinées à l'entraînement (30%).
--test_count 0.5: Le pourcentage d'images destinées aux tests (50%).
--image_count 200: Le nombre d'images à utiliser à partir du jeu de données brut (200 images seront utilisées).
--blur_count 0.5: Le pourcentage d'images avec effet de flou (50% des images auront un effet de flou).

Étape 3: Résultats

L'image est recadrée et floutée.
![test](./MicrosoftTeams-image%20(2).png)
