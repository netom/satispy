#!/usr/bin/env bash

. venv.sh

python -m build --sdist
python -m build --wheel
