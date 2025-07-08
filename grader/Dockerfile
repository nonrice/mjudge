# Use official Python image
FROM python:3.11-slim

# Set work directory inside container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the grader app
COPY . .


# Command to run the polling script
CMD ["python", "-u", "run.py"]
