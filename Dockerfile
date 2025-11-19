FROM python:3.11-slim-bullseye

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system packages required for Pillow, WeasyPrint and psycopg2
# Use Debian-compatible package names and make apt update tolerant to release info changes
RUN apt-get update --allow-releaseinfo-change && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    apt-transport-https \
    build-essential \
    gcc \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip dependencies
COPY requirements.txt ./
RUN python -m pip install --upgrade pip setuptools wheel
# Use prefer-binary and no-cache to favour prebuilt wheels and reduce layer size
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

WORKDIR /app/job1

# Add entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]