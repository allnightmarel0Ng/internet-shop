FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /app

ARG EXPOSE_PORT
ARG PORT

RUN if [ -n "$EXPOSE_PORT" ]; then \
        echo "EXPOSE $PORT" >> /app/Dockerfile.tmp; \
    fi

ARG NAME
COPY ./cmd/${NAME}/main.py ./main.py
CMD ["python3", "-u", "./main.py"]