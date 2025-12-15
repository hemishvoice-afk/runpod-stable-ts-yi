# Base image with Python, PyTorch, and CUDA support
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Install system dependencies required for Whisper/Audio processing
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
# We install stable-ts directly from the user's provided organization repo
# to ensure we have their specific version/fork if applicable.
# 'scipy' is often required for some audio operations.
RUN pip install --no-cache-dir \
    runpod \
    scipy \
    git+https://github.com/ivrit-ai/stable-ts.git

# Copy builder script and bake the model into the image
# This ensures faster cold starts by pre-downloading the large model
COPY builder.py .
RUN python builder.py

# Copy application source code
COPY src/ .

# Command to start the RunPod handler
CMD [ "python", "-u", "handler.py" ]
