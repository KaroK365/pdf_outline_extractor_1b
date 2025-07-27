# Adobe India Hackathon 2025 - Round 1A
# Heuristic-only PDF Outline Extractor
FROM python:3.9-slim

LABEL maintainer="Adobe India Hackathon Team"
LABEL version="2.0.0"
LABEL description="Persona-Driven PDF Document Intelligence"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# This makes the model available at /app/models/ inside the container
RUN mkdir -p /app/models && \
    python -c "from sentence_transformers import SentenceTransformer; model_name = 'all-MiniLM-L6-v2'; model = SentenceTransformer(model_name); model.save('/app/models/' + model_name)"


# Copy source code
COPY src/ ./src/
COPY main.py .
COPY run.sh .

# Make run script executable
RUN chmod +x run.sh

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=4

# Create input and output directories
COPY input/ ./input/
COPY output/ ./output/

# Set default command
CMD ["./run.sh"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, '/app/src'); from extractor import extract_outline; print('OK')" || exit 1

# Expose no ports (file-based processing)
# EXPOSE - not needed for this application

# Add metadata
LABEL org.opencontainers.image.title="PDF Outline Extractor"
LABEL org.opencontainers.image.description="Persona-Driven PDF Document Intelligence for Adobe India Hackathon 2025"
LABEL org.opencontainers.image.version="2.0.0"
LABEL org.opencontainers.image.vendor="Adobe India Hackathon Team"
