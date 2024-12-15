#!/bin/sh
echo 'starting'

. venv/bin/activate

printenv GOOGLE_JSON > /opt/google.json

chmod 644 /opt/google.json

python3 server.py srv --port 8080 --debug