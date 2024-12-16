#!/bin/sh
echo 'starting'

echo "STARTED00000000"

printenv GOOGLE_JSON
echo "11111"
printenv GOOGLE_JSON > /opt/google.json
echo "22222"
cat /opt/google.json

chmod 644 /opt/google.json

. venv/bin/activate
python3 server.py srv --port 8080 --debug
