#!/bin/sh
set -e

gunicorn -c gunicorn.conf.py app:app
