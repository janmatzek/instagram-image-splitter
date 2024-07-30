# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install venv
RUN apt-get update && apt-get install -y python3-venv

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment and install dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run uvicorn server
CMD ["/app/venv/bin/uvicorn", "splitter_api:app", "--host", "0.0.0.0", "--port", "8000"]
