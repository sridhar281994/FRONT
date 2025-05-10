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
ENV LANG C.UTF-8
# Install Python dependencies
RUN pip install --no-cache-dir cython buildozer
# Patch Buildozer to skip root confirmation
RUN python3 -c "import buildozer; f = buildozer.__file__; with open(f, 'r') as file: content = file.read(); content = content.replace(\"cont = input('Are you sure you want to continue [y/n]?')\", \"cont = 'y'\"); with open(f, 'w') as file: file.write(content)"
# Default workdir
WORKDIR /app
