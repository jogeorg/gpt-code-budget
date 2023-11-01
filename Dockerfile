# Use a Node.js image with Python and pip
FROM node:20.9.0

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3-venv && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-full && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your project files
COPY frontend /app/frontend
COPY gpt_code_ui /app/gpt_code_ui
COPY .env /app
COPY requirements.txt /app
COPY setup.py /app
COPY Makefile /app/frontend
COPY README.md /app

# Create and activate a virtual environment
RUN python3 -m venv /app/venv
SHELL ["/bin/bash", "-c"]
RUN source /app/venv/bin/activate
SHELL ["/bin/sh", "-c"]

# Install Python dependencies within the virtual environment
RUN pip install -r requirements.txt --break-system-packages
RUN pip install -e . --break-system-packages

WORKDIR /app/frontend
# Run the frontend compilation
RUN npm install -g typescript vite

RUN make compile_frontend

# Deactivate the virtual environment
RUN deactivate

# Set the working directory back to /app
WORKDIR /app

# Define the command to run your application
CMD [ "gptcode" ]
