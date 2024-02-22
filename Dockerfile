# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y netcat gcc \
    && apt-get clean

# Install Python dependencies
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY ./app /app

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
