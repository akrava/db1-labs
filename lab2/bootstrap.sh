#!/bin/bash

if [[ ! -d venv ]]; then
    virtualenv venv
    source venv/bin/activate
    pipenv install --dev
else
    source venv/bin/activate
fi
python src/main.py