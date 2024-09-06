#!/usr/bin/env bash

set -Eeou pipefail

# run serve
if [[ "${APP__APP_ENV}" = "dev" ]]; then
  PYTHONPATH=. exec uvicorn app.main:app --host 0.0.0.0 --reload
elif [[ "${APP__APP_ENV}" = "prod" ]]; then
  PYTHONPATH=. exec gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py app.main:app
else
  echo "choose dev or prod"
  exit 1
fi
