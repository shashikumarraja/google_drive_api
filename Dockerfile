FROM python:latest
RUN apt-get update -y
RUN apt-get install -y vim jq
COPY requirements.txt /google_drive_api/
WORKDIR /google_drive_api
RUN pip install -r /google_drive_api/requirements.txt
ENTRYPOINT [ "python3" ]
STOPSIGNAL SIGINT