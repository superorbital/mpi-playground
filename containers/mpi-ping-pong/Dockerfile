FROM python:3-slim-bullseye

RUN adduser --home /app \
    --shell /bin/bash \
    --uid 5000 \
    --disabled-login \
    --gecos "container user" \
    container

RUN apt update -y && \
    apt install -y openmpi-bin libopenmpi-dev

# Install OpenSSH for MPI to communicate between containers
RUN apt install -y --no-install-recommends openssh-client openssh-server && \
    mkdir -p /var/run/sshd && \
    mkdir -p /root/.ssh

# Allow OpenSSH to talk to containers without asking for confirmation
# by disabling StrictHostKeyChecking.
# mpi-operator mounts the .ssh folder from a Secret. For that to work, we need
# to disable UserKnownHostsFile to avoid write permissions.
# Disabling StrictModes avoids directory and files read permission checks.
RUN sed -i 's/[ #]\(.*StrictHostKeyChecking \).*/ \1no/g' /etc/ssh/ssh_config && \
    echo "    UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config && \
    echo "    Port 2222" >> /etc/ssh/ssh_config && \
    sed -i 's/#\(StrictModes \).*/\1no/g' /etc/ssh/sshd_config && \
    echo "Port 2222" >> /etc/ssh/sshd_config

WORKDIR /app

COPY sshd_config /app/.sshd_config
COPY ssh_config /app/.ssh/config
COPY ssh_config /root/.ssh/config

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY mpi-ping-pong.py /app

RUN chown -R container:container /app

CMD [ "mpirun", "-np", "1", "/app/mpi-ping-pong.py" ]
