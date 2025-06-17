FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy your worker code
COPY . .

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# The container entrypoint will accept a submission ID
ENTRYPOINT ["python", "worker.py"]
