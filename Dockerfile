FROM python:3.9-slim
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    openjdk-17-jdk-headless \
    unzip \
    zip \
    libncurses5 \
    libstdc++6 \
    libffi-dev \
    libssl-dev \
    libsqlite3-dev \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libpng-dev \
    liblzma-dev \
    libgdbm-dev \
    libnss3-dev \
    libreadline-dev \
    libbz2-dev \
    libgdbm-compat-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
# Set locale
ENV LANG=C.UTF-8
# Install Python dependencies
RUN pip install --no-cache-dir cython buildozer
# Patch Buildozer to auto-accept root confirmation
RUN echo "import buildozer; f = buildozer.__file__.replace('__init__.pyc', '__init__.py'); \
text = open(f).read(); text = text.replace(\"cont = input('Are you sure you want to continue [y/n]?')\", \"cont = 'y'\"); \
open(f, 'w').write(text)" > /tmp/patch.py && python3 /tmp/patch.py
# Set working directory
WORKDIR /app
