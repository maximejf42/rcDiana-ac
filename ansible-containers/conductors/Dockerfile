ARG RCD_ARCH=amd64
FROM resin/${RCD_ARCH}-debian:stretch
MAINTAINER Derek Merck <derek_merck@brown.edu>

# Not sure what this is for
ENV ANSIBLE_CONTAINER=1

RUN apt-get update -y && apt-get install -y \
        apt-utils \
        build-essential \
        cmake \
        pkg-config \
        curl \
        git \
        libffi-dev \
        libpopt0 \
        libssl-dev \
        rsync \
        sudo \
        wget \
        bzip2 \
        ca-certificates \
        python2.7 \
        python-apt \
        python-dev \
        ssh \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN cd /usr/bin \
    && rm -f lsb_release \
    && ln -fs python2.7 python

RUN (curl https://bootstrap.pypa.io/get-pip.py | python - --no-cache-dir ) \
    && pip install --upgrade pip

RUN (curl https://get.docker.com | sh )

RUN mkdir -p /etc/ansible/roles /_ansible

COPY . /_ansible

RUN cd /_ansible \
    && pip install --no-cache-dir -r pkg_requirements.txt \
    && ansible-galaxy install -p /etc/ansible/roles -r role_requirements.yml

COPY . /_ansible

RUN cd /_ansible \
    && git clone https://github.com/ansible/ansible-container.git \
    && cd /_ansible/ansible-container \
    && sed -i "s/pip.req/pip._internal.req/" setup.py \
    && pip install -e .

# Should be pip install -e .[docker], maybe develop includes them all?

