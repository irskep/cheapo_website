# pull official base image
FROM python:3.9.13-alpine

# install dependencies for maintenance (not needed to run the app)
RUN apk add --no-cache make sqlite

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create the code directory - and switch to it
RUN mkdir -p /code
WORKDIR /code

# install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

# copy project
COPY . /code/

EXPOSE 8080

CMD ["gunicorn", "--bind", ":8080", "server:app"]