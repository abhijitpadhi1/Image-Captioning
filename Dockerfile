FROM python:3.10-slim

WORKDIR /app

# Copy backend
COPY backend ./backend

# Copy frontend build
COPY frontend/dist ./frontend/dist

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN echo "Rebuilding dependencies..."

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose HF port
EXPOSE 7860

# Start server
CMD ["uvicorn", "backend.app.api:app", "--host", "0.0.0.0", "--port", "7860"]