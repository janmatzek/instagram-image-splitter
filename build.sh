#!/bin/bash

# Define variables
IMAGE_NAME="insta-splitter"
CONTAINER_NAME="insta-splitter-container"
DOCKERFILE_PATH="."

# Build the Docker image
echo "Building the Docker image..."
sudo docker build -t $IMAGE_NAME $DOCKERFILE_PATH

# Stop and remove the old container if it exists
echo "Stopping and removing the old container if it exists..."
sudo docker stop $CONTAINER_NAME && sudo docker rm $CONTAINER_NAME

# Run the new container
echo "Running the new container..."
sudo docker run -d --name $CONTAINER_NAME -p 8000:8000 $IMAGE_NAME

echo "Container build completed!"
