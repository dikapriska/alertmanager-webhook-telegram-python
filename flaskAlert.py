import telegram, json, logging, os
from time import sleep
from telegram.error import RetryAfter, TimedOut, NetworkError
from dateutil import parser
from flask import Flask
from flask import request
from flask_basicauth import BasicAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
basic_auth = BasicAuth(app)

chatID = os.getenv('TELEGRAM_CHAT_ID')

message_thread_id = os.getenv('TELEGRAM_MESSAGE_THREAD_ID') or None

app.config['BASIC_AUTH_FORCE'] = os.getenv('BASIC_AUTH_FORCE')
app.config['BASIC_AUTH_USERNAME'] = os.getenv('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.getenv('BASIC_AUTH_PASSWORD')

bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

@app.route('/alert', methods = ['POST'])
def postAlertmanager():

    try:
        content = json.loads(request.get_data())
        for alert in content['alerts']:
            message = "Status: "+alert['status']+"\n"
            if 'name' in alert['labels']:
                message += "Instance: "+alert['labels']['instance']+"("+alert['labels']['name']+")\n"
            else:
                message += "Instance: "+alert['labels']['instance']+"\n"
            if 'info' in alert['annotations']:
                message += "Info: "+alert['annotations']['info']+"\n"
            if 'summary' in alert['annotations']:
                message += "Summary: "+alert['annotations']['summary']+"\n"                
            if 'description' in alert['annotations']:
                message += "Description: "+alert['annotations']['description']+"\n"
            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Resolved: "+correctDate
            elif alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Started: "+correctDate
            if message_thread_id:
                bot.sendMessage(chat_id=chatID, text=message, message_thread_id=message_thread_id)
            else:
                bot.sendMessage(chat_id=chatID, text=message)
        return "Alert OK", 200
    except RetryAfter:
        sleep(30)
        if message_thread_id:
            bot.sendMessage(chat_id=chatID, text=message, message_thread_id=message_thread_id)
        else:
            bot.sendMessage(chat_id=chatID, text=message)
        return "Alert OK", 200
    except TimedOut as e:
        sleep(60)
        if message_thread_id:
            bot.sendMessage(chat_id=chatID, text=message, message_thread_id=message_thread_id)
        else:
            bot.sendMessage(chat_id=chatID, text=message)
        return "Alert OK", 200
    except NetworkError as e:
        sleep(60)
        if message_thread_id:
            bot.sendMessage(chat_id=chatID, text=message, message_thread_id=message_thread_id)
        else:
            bot.sendMessage(chat_id=chatID, text=message)
        return "Alert OK", 200
    except Exception as error:       
        error_msg = "Error: "+str(error)
        if message_thread_id:
            bot.sendMessage(chat_id=chatID, text=error_msg, message_thread_id=message_thread_id)
        else:
            bot.sendMessage(chat_id=chatID, text=error_msg)
        app.logger.info("\t%s",error)
        return "Alert fail", 200

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=9119)
