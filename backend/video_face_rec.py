#! /usr/bin/python

# import the necessary packages
import face_recognition
import imutils
import pickle
import cv2
import os
import logging
from collections import Counter

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)


def analyze_video(video_path):
    # Initialize 'currentname' to trigger only when a new person is identified.
    # Determine faces from encodings.pickle file model created from train_model.py
    encodings_file_path = os.getenv("ENCODINGS_FILE_PATH", "encodings.pickle")
    # use this xml file
    cascade = "backend/haarcascade_frontalface_default.xml"

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    log.info("Loading encodings + face detector...")
    data = pickle.loads(open(encodings_file_path, "rb").read())
    detector = cv2.CascadeClassifier(cascade)

    # Starting to play the video and analyzing it
    log.info("Starting video stream...")
    cap = cv2.VideoCapture(video_path)

    # Initializing names array
    names = []

    # loop over frames from the video file stream
    while cap.isOpened():
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)

        ret, frame = cap.read()
        if ret:
            frame = imutils.resize(frame, width=500)

            # convert the input frame from (1) BGR to grayscale (for face
            # detection) and (2) from BGR to RGB (for face recognition)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # detect faces in the grayscale frame
            rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

            # OpenCV returns bounding box coordinates in (x, y, w, h) order
            # but we need them in (top, right, bottom, left) order, so we
            # need to do a bit of reordering
            boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"],
                                                         encoding)
                name = "Unknown"  # if face is not recognized, then print Unknown

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    matched_idxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matched_idxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key=counts.get)

                # If someone in your dataset is identified, print their name on the screen
                # print(name)

                # update the list of names
                names.append(name)
        else:
            break

    # Output names by number of appearances
    counts = Counter(names)
    result = sorted(counts, key=counts.get, reverse=True)
    log.info("Video processed. most of the chances are that this person is " + result[0])
    # do a bit of cleanup
    cap.release()
    cv2.destroyAllWindows()

    return result[0]
