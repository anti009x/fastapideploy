FROM python:3.11.5

# WORKDIR /app
# COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
