FROM python:3.8-slim AS bot

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100

ENV API_TOKEN ${API_TOKEN}
ENV LOG_FOLDER ${LOG_FOLDER}
ENV LOG_FILE ${LOG_FILE}
ENV MAX_FILE_SIZE ${MAX_FILE_SIZE}
ENV ALLOWED_USERS ${ALLOWED_USERS}

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv

RUN mkdir -p /usr/app
ADD . /usr/app
WORKDIR /usr/app

RUN pip3 install -r requirements.txt
RUN chmod +x /usr/app/main.py

CMD python3 /usr/app/main.py;
