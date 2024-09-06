#!/usr/bin/env bash

set -Eeou pipefail

# update apt
sudo apt update

# install poetry
pip install poetry
poetry config virtualenvs.in-project true
