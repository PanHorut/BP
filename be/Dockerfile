# Use an official Python image as the base image
FROM python:3.11-slim

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the content of your current directory into the container's working directory
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the application
EXPOSE 8000

# Command to run the application (adjust this to your Django project)
CMD ["gunicorn", "your_project_name.wsgi", "--bind", "0.0.0.0:8000"]
