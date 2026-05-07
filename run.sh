#!/bin/bash

# Set environment variables for compatibility with both old and new naming
export FLASK_SECRET_KEY=${FLASK_SECRET_KEY:-changeKeyHeere}
export TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID:-${chatid:--xchatIDx}}
export TELEGRAM_MESSAGE_THREAD_ID=${TELEGRAM_MESSAGE_THREAD_ID:-}
export BASIC_AUTH_FORCE=${BASIC_AUTH_FORCE:-True}
export BASIC_AUTH_USERNAME=${BASIC_AUTH_USERNAME:-${username:-XXXUSERNAME}}
export BASIC_AUTH_PASSWORD=${BASIC_AUTH_PASSWORD:-${password:-XXXPASSWORD}}
export TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN:-${bottoken:-botToken}}

# Validate required variables
if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ "$TELEGRAM_BOT_TOKEN" == "botToken" ]; then
  echo "FAIL: TELEGRAM_BOT_TOKEN or bottoken is not set"
  exit 1
fi

if [ -z "$TELEGRAM_CHAT_ID" ] || [ "$TELEGRAM_CHAT_ID" == "-xchatIDx" ]; then
  echo "FAIL: TELEGRAM_CHAT_ID or chatid is not set"
  exit 2
fi

echo "Starting Alertmanager Telegram Webhook"
echo "Chat ID: $TELEGRAM_CHAT_ID"
if [ -n "$TELEGRAM_MESSAGE_THREAD_ID" ]; then
  echo "Message Thread ID: $TELEGRAM_MESSAGE_THREAD_ID"
fi

exec /usr/local/bin/gunicorn -w 4 -b 0.0.0.0:9119 flaskAlert:app
