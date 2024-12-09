# Use a base image that supports your app
FROM python:3.11-slim

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the necessary port (e.g., 8000 for Django)
EXPOSE 8000

# Use Gunicorn to run the Django application
CMD ["gunicorn", "be.wsgi:application", "--bind", "0.0.0.0:8000"]
