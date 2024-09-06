FROM python:3.12-bookworm as builder

COPY poetry.lock /
COPY pyproject.toml /

RUN pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --without dev && \
    rm -f /poetry.lock /pyproject.toml && \
    pip3 uninstall -y poetry

FROM python:3.12-slim-bookworm as runner

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages 
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn 
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

RUN apt update && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /etc/apt/apt.conf

RUN useradd -r -s /bin/false gunicorn

COPY code_caster /opt/code_caster

USER gunicorn
WORKDIR /opt/code_caster

EXPOSE 8000
CMD ["/bin/bash", "start.sh"]
