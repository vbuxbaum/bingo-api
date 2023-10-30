FROM python:3.9-alpine3.13
LABEL maintainer="github.com/vbuxbaum"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./dev-requirements.txt /tmp/dev-requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
ARG DEV=false
RUN echo 'starting...' && \
    apk add --update build-base && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip setuptools wheel && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/dev-requirements.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        fastapi-user

ENV PATH="/py/bin:$PATH"

USER fastapi-user