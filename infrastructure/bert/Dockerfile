FROM tensorflow/tensorflow:1.12.0-py3

RUN pip install --no-cache-dir bert-serving-server

COPY . /bert

WORKDIR /bert

ADD https://s3.eu-central-1.wasabisys.com/crowdeval-models/stsb-bert-base-tf.zip .
RUN mkdir stsb-bert-base-tf
RUN unzip stsb-bert-base-tf.zip -d stsb-bert-base-tf/

RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]