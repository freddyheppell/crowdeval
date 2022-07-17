FROM jinaai/jina:3.6-py38-standard

WORKDIR /workspace
COPY . /workspace

# Manually install pytorch since the version the TransformerTorchEncoder executor requests doesn't install in the container
RUN pip3 install torch==1.9.0 --extra-index-url https://download.pytorch.org/whl/torch_stable.html
# Also install its other dependencies
RUN pip3 install transformers>=4.12.0

# Pull the containers now to prevent downloading each time the container starts
RUN jina hub pull jinahub://TransformerTorchEncoder

CMD ["flow", "--uses", "flow.jina.yml"]