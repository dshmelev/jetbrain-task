FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y curl net-tools iproute2 dnsutils && \
    rm -rf /var/lib/apt/lists/* \

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/.  .

EXPOSE 8000

CMD ["python", "main.py"]