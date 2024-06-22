FROM python:3.10-bullseye

WORKDIR /app

COPY requirements.txt .
# Update default packages
RUN apt-get update

# Get Ubuntu packages
RUN apt-get install -y \
    build-essential \
    curl

# Update new packages
RUN apt-get update

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install uvicorn
RUN pip install "uvicorn[standard]"
RUN pip install fastapi 

# Download and set up ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install ngrok

EXPOSE 8000
RUN ["ngrok config add-authtoken 2hQxB1ZLybpRWy9xcLaHVnXZtw0_5r1v1e2FWMZsXmCWPYSdL && RUN uvicorn main:app --reload && ngrok http http://localhost:8000"]