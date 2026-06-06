#!/bin/bash
set -euo pipefail

BOT_DIR="/opt/botmanagment"

apt-get update
apt-get install -y python3 python3-pip python3-venv

mkdir -p "$BOT_DIR"
cp -f main.py config.py handlers.py states.py keyboards.py requirements.txt "$BOT_DIR/"

python3 -m venv "$BOT_DIR/venv"
"$BOT_DIR/venv/bin/pip" install --upgrade pip
"$BOT_DIR/venv/bin/pip" install -r "$BOT_DIR/requirements.txt"

cp -f deploy/bot.service /etc/systemd/system/botmanagment.service
systemctl daemon-reload
systemctl enable botmanagment
systemctl restart botmanagment
systemctl status botmanagment --no-pager

echo "Бот установлен и запущен."
