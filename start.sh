#!/bin/sh
echo 'starting'

. venv/bin/activate

printenv GOOGLE_JSON > /opt/google.json

#sed -z 's/\n/\\n/g; s/..$//' /opt/google.json > /opt/google.json
chmod 644 /opt/google.json
echo "\n\n"
cat /opt/google.json
echo "\n\n"

python3 server.py srv --port 8080 --debug