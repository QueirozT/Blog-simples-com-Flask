#!/bin/bash

flask db upgrade

exec gunicorn -b :8000 --access-logfile - --error-logfile - wsgi:app