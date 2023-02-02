apt-get update && \
  apt-get install -y libgeos-dev && \
  pip install -r requirements.txt && \
  pip install grpcio_tools