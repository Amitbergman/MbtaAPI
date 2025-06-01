# Use official Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all python scripts into the container
COPY *.py .

# Run tests
RUN python tests.py

# Run the python app
CMD ["python", "app.py"]