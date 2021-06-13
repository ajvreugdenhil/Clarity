#!/usr/bin/env bash
cd "$(dirname "$0")"
service nginx start
uwsgi --ini uwsgi.ini