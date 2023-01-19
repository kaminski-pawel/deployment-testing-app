FROM python:3.9-alpine3.13
LABEL maintainer="pawelkaminski@tipi.software"

ENV PYTHONUNBUFFERED 1

COPY ./requirements /tmp/requirements
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements/dev.txt; \
        else /py/bin/pip install -r /tmp/requirements/prod.txt; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        app-user

ENV PATH="/py/bin:$PATH"

USER app-user

CMD ["run.sh"]
