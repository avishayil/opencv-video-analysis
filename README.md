# OpenCV Video Analysis
Use OpenCV-Python and Flask to create an application that collects photos from the computer / phone / tablet camera, training a local computer vision model to later analyze photos and videos, recognizing the names of those people.

## Environment
* Docker
* Python 2.7.18
* OpenCV 4.2.0
* Should work also on Raspberry PI

## How to Run 

### Running with Python

1. Install python requirements:

    ```
    pip install -r requirements.txt
    pip install opencv-python-headless==4.2.0.32
    ```

2. Run the app:

    ```
    export ENCODINGS_FILE_PATH="encodings.pickle" # The path to the file must exist (create an empty file with `touch encodings.pickle`)
    export DATASET_FOLDER_PATH="dataset" # The path to the folder must exist (create an empty folder with `mkdir -p dataset`)
    export MODEL="hog" # Training model. `hog` for using CPU, `cnn` for using GPU.
    export LOGLEVEL="INFO" # Logging level
    python backend/app.py
    ```
   
    - Frontend should be available on `localhost:5000`
    - API calls should be visible on the terminal console

### Running with Docker

Docker image of this application is available at `https://hub.docker.com/r/avishayil/opencv-video-analysis`

1. Copy `docker/.env.example` to `docker/.env` and change the logging level, dataset and encodings location, and model (`hog` (default) or `cnn` (GPU, slower))

2. Run the container with `docker-compose`:

    ```
    cd docker
    cp .env.example .env
    docker-compose up -d
    ```

    - Frontend should be available on `localhost:5000`
    - API calls should be visible on the `docker logs` console

## Usage

### Training the Model

1. Enter the user name on the textbox
2. Press the `Capture` button at least 30 times when moving your face around in different positions
3. Press the `Train` button to analyze the new added photos

### Playground

1. Navigate to `Playground` link on the web application
2. Capture a photo. If the face on the photo is recognized, you'll get it on the `Snapshot` box response. If not, `Unknown` will appear.

### API

#### Video Analysis

1. Send a `POST` request to `localhost:5000/analyze_video` with the following syntax:
   ````
   {
     "url": "https://path_to_video_url.mp4"
   }
   ````
   MP4 should be working fine, but the rest of formats are currently untested.

#### Photo Analysis

1. Send a `POST` request to `localhost:5000/analyze_photo` with the following syntax:
   ````
   {
     "url": "https://path_to_photo_url.jpg"
   }
   ````
   JPG should be working fine, but the rest of formats are currently untested.
