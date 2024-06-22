# Use an official Python runtime as a parent image
FROM python:3.10-bullseye

# Set the working directory in the container
WORKDIR /app
RUN echo "made working dir"

# Copy the current directory contents into the container at /app
COPY . .

RUN echo "starting to install dependencies"
RUN pip install -r requirements.txt

RUN echo "installed requirements"
# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    curl && \
    curl https://sh.rustup.rs -sSf | bash -s -- -y && \
    apt-get update && \
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install ngrok && \
    pip install --no-cache-dir uvicorn "uvicorn[standard]" fastapi

# Ensure the start script is executable
RUN chmod +x start.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run start.sh when the container launches
CMD ["./start.sh"]
