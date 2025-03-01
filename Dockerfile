FROM nikolaik/python-nodejs:python3.11-nodejs19
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        gcc \
        python3-dev \
        tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /app/

WORKDIR /app/

RUN pip3 install --no-cache-dir -U -r requirements.txt

ENTRYPOINT ["/usr/bin/tini", "--"]


CMD ["bash", "start"]
