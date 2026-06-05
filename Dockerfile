FROM python:3.11-alpine

WORKDIR /pb
ADD . /build

RUN apk add --no-cache --virtual .build-deps git gcc musl-dev \
    && pip install --upgrade pip setuptools setuptools-scm \
    && pip install /build \
    && apk del .build-deps

CMD ["python", "-m", "pb"]
