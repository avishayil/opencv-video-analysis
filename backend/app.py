import os
import logging
from flask import Flask, render_template, jsonify, request
from counter import Counter
from train_model import train
from video_face_rec import analyze_video
from photo_face_rec import analyze_photo
from urlparse import urlparse
from urllib import urlretrieve
from base64 import b64decode

logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))
log = logging.getLogger(__name__)

counter = Counter()
dataset_folder_path = os.getenv("DATASET_FOLDER_PATH", "dataset")

app = Flask(__name__,
            static_url_path='',
            static_folder='../frontend/static',
            template_folder='../frontend/templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/playground')
def playground():
    return render_template('playground.html')


@app.route('/snapshot', methods=['POST'])
def take_snapshot():
    json = request.get_json()
    name = json['name']
    image = json['image']
    if not os.path.exists(dataset_folder_path + '/' + name):
        os.makedirs(dataset_folder_path + '/' + name)
    img_name = dataset_folder_path + '/' + name + "/image_{}.jpg".format(counter.count())

    header, encoded = image.split(",", 1)
    data = b64decode(encoded)

    with open(img_name, "wb") as f:
        f.write(data)
    return jsonify(result="snapshot taken")


@app.route('/train_model', methods=['POST'])
def train_model():
    train()
    return jsonify(result="train completed")


@app.route('/analyze_video', methods=['POST'])
def get_video_analysis():
    json = request.get_json()
    url = json['url']
    parsed_url = urlparse(url)
    url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parsed_url.query
    try:
        urlretrieve(url, 'video.mp4')
        output = analyze_video('video.mp4')
        f = open("last_video_person.txt", "w")
        f.write(output)
        f.close()
    except Exception, e:
        log.error('Failed to retrieve or analyze video: ' + str(e))
        output = 'Failed to retrieve or analyze video'

    return {'response': output}


@app.route('/analyze_photo', methods=['POST'])
def get_photo_analysis():
    json = request.get_json()
    url = json['url']
    parsed_url = urlparse(url)
    url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path + "?" + parsed_url.query
    try:
        urlretrieve(url, 'photo.jpg')
        output = analyze_photo('photo.jpg')
        f = open("last_photo_person.txt", "w")
        f.write(output)
        f.close()
    except Exception, e:
        log.error('Failed to retrieve or analyze photo: ' + str(e))
        output = 'Failed to retrieve or analyze photo'

    return {'response': output}


@app.route('/get_latest_video_person', methods=['GET'])
def get_latest_video_person():
    try:
        f = open("last_video_person.txt", "r")
        output = f.read()
    except Exception, e:
        log.error('Failed to get latest person: ' + str(e))
        output = 'Failed to get latest person'

    return {'response': output}

@app.route('/get_latest_photo_person', methods=['GET'])
def get_latest_photo_person():
    try:
        f = open("last_photo_person.txt", "r")
        output = f.read()
    except Exception, e:
        log.error('Failed to get latest person: ' + str(e))
        output = 'Failed to get latest person'

    return {'response': output}

@app.route('/analyze_photo_data_url', methods=['POST'])
def get_data_url_analysis():
    json = request.get_json()
    data_url = json['image']
    try:
        header, encoded = data_url.split(",", 1)
        data = b64decode(encoded)

        with open('temp.jpg', "wb") as f:
            f.write(data)

        output = analyze_photo('temp.jpg')
    except Exception, e:
        log.error('Failed to retrieve or analyze photo: ' + str(e))
        output = 'Failed to retrieve or analyze photo'

    return {'response': output}


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', threaded=True)
