# Use lightweight Python base image
FROM python:3.10-slim

# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies required for OpenCV & EasyOCR
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into container
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "myapp.py", "--server.port=8501", "--server.address=0.0.0.0"]