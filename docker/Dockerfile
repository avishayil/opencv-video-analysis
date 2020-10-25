# syntax = docker/dockerfile:experimental

FROM mohaseeb/raspberrypi3-python-opencv:latest

RUN apt update \
    && apt upgrade -y

RUN pip2 install --upgrade pip wheel

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app
RUN pip2 -v --log /tmp/pip.log install --no-cache-dir -r requirements.txt

ENV PORT 5000
ENV ENCODINGS_FILE_PATH "/data/encodings/encodings.pickle"
ENV DATASET_FOLDER_PATH "/data/dataset"
ENV LOGLEVEL "$LOGLEVEL"
ENV MODEL "$MODEL"

ADD . /usr/src/app/

EXPOSE 5000

CMD [ "python2", "backend/app.py" ]
