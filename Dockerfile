# Build Stage
FROM node:latest as frontend

WORKDIR /front

COPY ./frontend /front
COPY ./frontend/dist /front

WORKDIR /front/frontend
RUN npm install
RUN npm run build

# Runtime Stage
FROM python:3.9 as backend

WORKDIR /app

# Copy your project files for the backend
COPY .env /app
COPY requirements.txt /app
COPY gpt_code_ui /app
COPY gpt_code_ui/__init__.py /app/gpt_code_ui/
COPY gpt_code_ui/main.py /app/gpt_code_ui/
COPY gpt_code_ui/kernel_program /app/gpt_code_ui/kernel_program/
COPY gpt_code_ui/webapp /app/gpt_code_ui/webapp/
COPY workspace /app
COPY setup.py /app
COPY README.md /app

# Install Python dependencies
RUN pip install -r requirements.txt
RUN pip install -e .

# Copy only necessary files from the frontend build
COPY --from=frontend /front/dist/ /app/gpt_code_ui/webapp/static/

EXPOSE 8080

# Set the command to run your backend application
CMD ["gptcode"]
