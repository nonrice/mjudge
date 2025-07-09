FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    g++ \
    openjdk-17-jdk \
    time \
 && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "worker.py"]
