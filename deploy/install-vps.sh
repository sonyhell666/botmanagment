#!/usr/bin/env bash
# Установка Python-бота на Ubuntu/Debian VPS (запускать на сервере от root)
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/sonyhell666/botmanagment.git}"
INSTALL_DIR="${INSTALL_DIR:-/opt/botmanagment}"

echo "==> Python и git"
apt-get update -qq
apt-get install -y -qq python3 python3-venv python3-pip git curl ca-certificates
python3 --version

echo "==> Клонирование репозитория"
mkdir -p "$(dirname "$INSTALL_DIR")"
if [ -d "$INSTALL_DIR/.git" ]; then
  cd "$INSTALL_DIR"
  git pull origin main
else
  git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

if [ ! -f .env ]; then
  cp .env.example .env
  echo ""
  echo "!!! Создан $INSTALL_DIR/.env — заполните BOT_TOKEN и сохраните:"
  echo " nano $INSTALL_DIR/.env"
  echo ""
  exit 1
fi

if grep -q "your_telegram_bot_token_here" .env; then
  echo "!!! Заполните BOT_TOKEN в $INSTALL_DIR/.env"
  exit 1
fi

echo "==> Виртуальное окружение"
python3 -m venv venv
venv/bin/pip install --upgrade pip -q
venv/bin/pip install -r requirements.txt -q

echo "==> systemd"
cp deploy/botmanagment.service /etc/systemd/system/botmanagment.service
systemctl daemon-reload
systemctl enable botmanagment
systemctl restart botmanagment

echo "==> Статус"
sleep 2
systemctl status botmanagment --no-pager || true
echo ""
echo "Логи: journalctl -u botmanagment -f"
