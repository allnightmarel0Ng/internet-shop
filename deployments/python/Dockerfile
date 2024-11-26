FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt /app/

RUN pip3 install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /app

ARG PORT
EXPOSE ${PORT}

ARG NAME
COPY ./cmd/${NAME}/main.py ./main.py
CMD ["python3", "./main.py"]