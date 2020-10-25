#! /usr/bin/python

from imutils import paths
import face_recognition
import pickle
import cv2
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)
model = os.environ.get("MODEL", "hog") # hog or cnn


def train():
    # our images are located in the dataset folder
    log.info("Start processing faces...")

    encodings_file_path = os.getenv("ENCODINGS_FILE_PATH", "encodings.pickle")
    dataset_folder_path = os.getenv("DATASET_FOLDER_PATH", "dataset")

    image_paths = list(paths.list_images(dataset_folder_path))

    # initialize the list of known encodings and known names
    known_encodings = []
    known_names = []

    # loop over the image paths
    for (i, image_path) in enumerate(image_paths):
        # extract the person name from the image path
        log.info("Processing image {}/{}".format(i + 1,
                                                 len(image_paths)))
        name = image_path.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
                                                model=model)

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            known_encodings.append(encoding)
            known_names.append(name)

    # dump the facial encodings + names to disk
    log.info("Serializing encodings...")
    data = {"encodings": known_encodings, "names": known_names}
    f = open(encodings_file_path, "wb")
    f.write(pickle.dumps(data))
    f.close()
