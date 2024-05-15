FROM python:3-slim-bullseye

RUN mkdir -p /app && \
    apt update -y && \
    apt install openmpi-bin libopenmpi-dev -y

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY mpi-ping-pong.py /app

CMD ["python", "/app/mpi-ping-pong.py"]

