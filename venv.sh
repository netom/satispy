#!/usr/bin/env bash

if [ ! -d venv ]; then
    python -m virtualenv venv
fi

. venv/bin/activate

pip install -r requirements.txt -r requirements-dev.txt
