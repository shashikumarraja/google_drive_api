FROM python:latest
RUN apt-get update -y
RUN apt-get install -y vim jq
# COPY . /src
COPY requirements.txt /src/
WORKDIR /src
RUN pip install -r /src/requirements.txt
ENTRYPOINT [ "python3" ]
STOPSIGNAL SIGINT