#!/usr/bin/fish
#export G4F_PROXY=socks5://127.0.0.1:25344
#export G4F_PROXY=http://127.0.0.1:25343
export SSL_CERT_FILE=data/russian_trusted_root_ca_pem.crt
source venv/bin/activate.fish
python main.py
