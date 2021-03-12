FROM tensorflow/tensorflow:1.12.0-py3

RUN pip install --no-cache-dir bert-serving-server

COPY . /bert

WORKDIR /bert

ADD https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-768_A-12.zip .
RUN mkdir uncased_L-12_H-768_A-12
RUN unzip uncased_L-12_H-768_A-12.zip -d uncased_L-12_H-768_A-12/

RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]