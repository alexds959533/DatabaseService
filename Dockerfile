# Dockerfile

# pull the official docker image
FROM python:3.10.1

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /venv
RUN pip install --upgrade pip


# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8010
VOLUME /data/db

# copy project
COPY . .