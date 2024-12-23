# Use the official slim Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install minimal system dependencies for psycopg2 and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and use a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Copy requirements first (to leverage Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the application port
EXPOSE 15001

# Run Gunicorn as the default application server
CMD ["gunicorn", "--bind", "0.0.0.0:15001", "--workers", "2", "gamerater.wsgi:application"]
