FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    glib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
# Install the CPU-only PyTorch build first. Otherwise ultralytics pulls the
# default CUDA build and its nvidia-* wheels (several GB), and the container
# has no GPU to use them.
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# watchfiles restarts the detector whenever a .py file under src/ changes
CMD ["watchfiles", "python src/detector.py", "src"]