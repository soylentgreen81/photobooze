#!/usr/bin/bash

source /home/photobooze/photobooze/venv/bin/activate
gunicorn --bind 0.0.0.0:8000 booze:booze
