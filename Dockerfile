FROM python:3.9-slim
# Set environment
ENV LANG C.UTF-8
ENV PATH="/usr/local/bin:$PATH"
ENV BUILDOZER_ALLOW_ROOT=1
# Install dependencies
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
    && rm -rf /var/lib/apt/lists/*
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip cython buildozer
# Set root-safe environment variable
ENV BUILDOZER_ALLOW_ROOT=1
# Install system packages
RUN apt-get update && apt-get install -y \
    build-essential git openjdk-17-jdk-headless unzip zip \
    libncurses5 libstdc++6 libffi-dev libssl-dev \
    libsqlite3-dev zlib1g-dev libjpeg-dev libfreetype6-dev \
    libpng-dev liblzma-dev libgdbm-dev libnss3-dev libreadline-dev \
    libbz2-dev libgdbm-compat-dev && \
    rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd -ms /bin/bash builduser
USER builduser
WORKDIR /home/builduser
# Install Python dependencies
RUN pip install --no-cache-dir cython buildozer
# Patch Buildozer to skip root prompt
RUN python3 -c "import buildozer, os; f = buildozer.__file__.replace('__init__.pyc', '__init__.py'); \
    content = open(f).read().replace(\"cont = input('Are you sure you want to continue [y/n]?')\", \"cont = 'y'\"); \
    open(f, 'w').write(content)"
WORKDIR /app
