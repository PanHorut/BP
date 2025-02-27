# Use a base image that supports your app
FROM python:3.11-slim

# Install system dependencies for mysqlclient and build tools
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    pkg-config \
    gcc \
    python3-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory (inside `/app`)
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application
COPY manage.py docker-entrypoint.sh /app/
COPY be /app/be
COPY api /app/api
COPY static /app/static
COPY staticfiles /app/staticfiles

# Expose the necessary port (8000 for Django)
EXPOSE 8000

# Make sure entrypoint script is executable
RUN chmod +x /app/docker-entrypoint.sh

# Use the entrypoint script to handle migrations and start the app
ENTRYPOINT ["/app/docker-entrypoint.sh"]
