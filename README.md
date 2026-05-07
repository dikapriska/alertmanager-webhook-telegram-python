# Alertmanager webhook for Telegram (Python Version)

![Docker Image CI](https://github.com/dikapriska/alertmanager-webhook-telegram-python/workflows/Docker%20Image%20CI/badge.svg)
![Code scanning - action](https://github.com/dikapriska/alertmanager-webhook-telegram-python/workflows/Code%20scanning%20-%20action/badge.svg)

GO Version (https://github.com/dikapriska/alertmanager-webhook-telegram-go)

Python version 3

## INSTALL

* pip install -r requirements.txt

Configuration with .env File
=============================
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and update the following variables:
   - `FLASK_SECRET_KEY`: Secret key for Flask application
   - `TELEGRAM_CHAT_ID`: Telegram chat ID (required, include the - prefix)
   - `TELEGRAM_MESSAGE_THREAD_ID`: Forum/Topic ID (optional, leave empty or remove if not using)
   - `BASIC_AUTH_FORCE`: Set to `True` to enable basic authentication, `False` to disable
   - `BASIC_AUTH_USERNAME`: Username for basic authentication
   - `BASIC_AUTH_PASSWORD`: Password for basic authentication
   - `TELEGRAM_BOT_TOKEN`: Telegram bot token

Forum/Topic Setup
=================
To send alerts to a specific forum/topic within a group:
1. Get the forum/topic ID from your Telegram group
2. Set `TELEGRAM_MESSAGE_THREAD_ID=12345` in your .env file (replace 12345 with your topic ID)
3. Leave `TELEGRAM_MESSAGE_THREAD_ID` empty or remove it to send to the default group

Disabling authentication
========================
Set `BASIC_AUTH_FORCE=False` in your .env file

Alertmanager configuration example
==================================

	receivers:
	- name: 'telegram-webhook'
	  webhook_configs:
	  - url: http://ipFlaskAlert:9119/alert
	    send_resolved: true
	    http_config:
	      basic_auth:
		username: 'admin'
		password: 'password'

One way to get the chat ID
==========================
1) Access https://web.telegram.org/
2) Click to specific chat to the left
3) At the url, you can get the chat ID(Ex: https://web.telegram.org/#/im?p=g1234567, so the chatID is 1234567)

Running
=======
* python flaskAlert.py

Installation Using Virtual Environment (venv)
==============================================
1. Create virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate virtual environment:
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - Windows:
     ```cmd
     venv\Scripts\activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python flaskAlert.py
   ```


Systemd Service Setup
=====================
1. Create service file:
   ```bash
   sudo nano /etc/systemd/system/webhook-telegram.service
   ```

2. Fill with the following configuration (adjust paths according to your project location):
   ```ini
   [Unit]
   Description=Alertmanager Telegram Webhook
   After=network.target

   [Service]
   Type=simple
   User=root
   Group=root
   WorkingDirectory=/opt/webhook-telegram
   ExecStart=/opt/webhook-telegram/venv/bin/python /opt/webhook-telegram/flaskAlert.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Save and close the file (Ctrl+X, then Y, then Enter)

4. Reload systemd and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable webhook-telegram
   sudo systemctl start webhook-telegram
   ```

5. Check service status:
   ```bash
   sudo systemctl status webhook-telegram
   ```

6. View logs:
   ```bash
   sudo journalctl -u webhook-telegram -f
   ```

Running on docker
=================
    git clone https://github.com/nopp/alertmanager-webhook-telegram.git
    cd alertmanager-webhook-telegram/docker/
    docker build -t alertmanager-webhook-telegram:1.0 .

    docker run -d --name telegram-bot \
    	-e "bottoken=telegramBotToken" \
    	-e "chatid=telegramChatID" \
    	-e "username=<username>" \
    	-e "password=<password>" \
    	-p 9119:9119 alertmanager-webhook-telegram:1.0

Example to test
===============
	curl -XPOST --data '{"status":"resolved","groupLabels":{"alertname":"instance_down"},"commonAnnotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"},"alerts":[{"status":"resolved","labels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"},"endsAt":"2019-07-01T16:16:19.376244942-03:00","generatorURL":"http://pmts.io:9090","startsAt":"2019-07-01T16:02:19.376245319-03:00","annotations":{"description":"i-0d7188fkl90bac100 of job ec2-sp-node_exporter has been down for more than 2 minutes.","summary":"Instance i-0d7188fkl90bac100 down"}}],"version":"4","receiver":"infra-alert","externalURL":"http://alm.io:9093","commonLabels":{"name":"olokinho01-prod","instance":"i-0d7188fkl90bac100","job":"ec2-sp-node_exporter","alertname":"instance_down","os":"linux","severity":"page"}}' http://username:password@flaskAlert:9119/alert
