FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

ARG PORT
EXPOSE ${PORT}

ARG NAME
COPY ./cmd/${NAME}/main.py ./main.py
CMD ["python3", "./main.py"]