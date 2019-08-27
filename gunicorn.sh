#!/usr/bin/bash

source /home/photobooze/photobooze/venv/bin/activate
gunicorn --worker-class eventlet -w 1 --no-sendfile  --bind 0.0.0.0:80 booze:booze
#/home/photobooze/photobooze/booze.py
