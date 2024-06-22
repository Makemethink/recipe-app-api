# Configuring a base image
FROM python:3.9-alpine3.13

# Adding meta data
LABEL maintainer="something.com"

# Python outputs are sent directly to the terminal without being buffered
ENV PYTHONUNBUFFERED 1

# Copy the requirements file to tmp folder
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# Set the working directory
WORKDIR /app

# Exposing the port
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    apk update && \
    apk add --no-cache \
    python3-dev \
    mariadb-dev \
    build-base && \
	/py/bin/pip install --upgrade pip && \
	/py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
	rm -rf /tmp && \
	adduser \
		--disabled-password \
		--no-create-home \
		django-user

ENV PATH="/py/bin:$PATH"

USER django-user

