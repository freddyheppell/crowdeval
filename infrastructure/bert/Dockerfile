FROM tensorflow/tensorflow:1.12.0-py3

RUN pip install --no-cache-dir bert-serving-server

COPY . /bert

WORKDIR /bert

ADD https://s3.eu-central-1.wasabisys.com/crowdeval-models/stsb_bert_base_converted.zip .
RUN mkdir stsb_bert_base_converted
RUN unzip stsb_bert_base_converted.zip -d stsb_bert_base_converted/

RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]