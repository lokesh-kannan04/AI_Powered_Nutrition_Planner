import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client

# Twilio configuration
TWILIO_CONFIG = {
    'ACCOUNT_SID': "ACb4bbd94a0a0f3b79829328b3857e6d92",
    'AUTH_TOKEN': "380760174c8c3fc9897cb423b82af33a",
    'WHATSAPP_NUMBER': "whatsapp:+14155238886"
}

# Hardcoded phone number (replace with actual number)
HARDCODED_NUMBER = "whatsapp:+919150109948"  # Example: "whatsapp:+911234567890"

def send_whatsapp_message():
    try:
        client = Client(TWILIO_CONFIG['ACCOUNT_SID'], TWILIO_CONFIG['AUTH_TOKEN'])
        now = datetime.datetime.now().time()

        scheduled_messages = {
            (15, 23): "Good morning! What did you have for breakfast?",
            (12, 0): "Hey! What did you eat for lunch?",
            (21, 39): "Good evening! What did you have for dinner?"
        }

        message = scheduled_messages.get((now.hour, now.minute))

        if message:
            client.messages.create(
                from_=TWILIO_CONFIG['WHATSAPP_NUMBER'],
                to=HARDCODED_NUMBER,
                body=message
            )
            print(f"Message sent to {HARDCODED_NUMBER}: {message}")

    except Exception as e:
        print(f"Error in send_whatsapp_message: {str(e)}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_whatsapp_message, 'cron', hour=15, minute=23)
    scheduler.add_job(send_whatsapp_message, 'cron', hour=12, minute=0)
    scheduler.add_job(send_whatsapp_message, 'cron', hour=21, minute=39)
    scheduler.start()
    print("Scheduler started successfully")

    try:
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler shut down successfully")
