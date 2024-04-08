# Use an official Node.js runtime as a parent image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN yarn

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define the command to run your JavaScript frontend
CMD ["yarn", "dev"]