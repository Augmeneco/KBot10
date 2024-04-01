#!/bin/bash

cd /srv/kbot/

export SSL_CERT_FILE=data/russian_trusted_root_ca_pem.crt
source venv/bin/activate

while true
do
    python main.py
    sleep 1
done
