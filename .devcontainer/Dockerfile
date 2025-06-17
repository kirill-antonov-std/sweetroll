# Base image with Python
FROM python:3.10.13-slim

# Install system dependencies
RUN apt update && apt install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK
RUN curl -sSL https://sdk.cloud.google.com | bash

# Set up working directory
WORKDIR /workspace

# Install Python dependencies (done in postCreateCommand too)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add non-root user for VS Code
RUN useradd -m vscode
USER vscode