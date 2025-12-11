#!/usr/bin/env bash

if [ ! -d venv ]; then
    python -m virtualenv venv
fi

. venv/bin/activate

pip install -r dev-requirements.txt
