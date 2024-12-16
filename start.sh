#!/bin/sh
echo 'starting'

#printenv GOOGLE_JSON
printenv GOOGLE_JSON > /opt/google.json

chmod 644 /opt/google.json

. venv/bin/activate
python3 server.py srv --port 8080 --debug
