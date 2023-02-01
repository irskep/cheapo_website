FROM python:3.9-alpine

COPY --from=flyio/litefs:0.3 /usr/local/bin/litefs /usr/local/bin/litefs
ADD etc/litefs.yml /etc/litefs.yml
RUN apk add bash fuse sqlite ca-certificates curl

WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt
COPY . .

ARG FLASK_SQLALCHEMY_DATABASE_URI=sqlite:////litefs/db
ENTRYPOINT litefs mount -- "gunicorn" "-b" "0.0.0.0:8000" "server:app"
