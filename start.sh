#!/bin/bash

cd /srv/kbot/

export SSL_CERT_FILE=/srv/kbot/data/russian_trusted_root_ca_pem.crt
source venv/bin/activate

while true
do
    #export DISPLAY=TownSquare-1:10.0
    xvfb-run python main.py
    sleep 1
done
