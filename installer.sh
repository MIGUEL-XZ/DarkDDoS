#!/bin/bash
# DarkDDoS Installer
# Uso: bash installer.sh

echo "[+] Instalando dependências..."
if [[ "$OSTYPE" == "linux-android"* ]]; then
    pkg update -y
    pkg install python3 python3-pip git -y
else
    sudo apt-get update
    sudo apt-get install python3 python3-pip git -y
fi

pip3 install --upgrade pip
pip3 install scapy requests cryptography

echo "[+] Clonando repositório..."
git clone https://github.com/seuuser/DarkDDoS.git
cd DarkDDoS
chmod +x DarkDDoS.py

echo "[+] Instalação concluída. Execute: python3 DarkDDoS.py --help"
