from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
from django.conf import settings
from django.contrib.sessions.models import Session
from api.models import FormData
import datetime

def send_whatsapp_message():
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    now = datetime.datetime.now().time()

    # Set messages for exact times
    scheduled_messages = {
        (15, 23): "Good morning! What did you have for breakfast?",
        (12, 0): "Hey! What did you eat for lunch?",
        (20, 2): "Good evening! What did you have for dinner?"
    }

    message = scheduled_messages.get((now.hour, now.minute))

    if message:
        active_sessions = Session.objects.filter(expire_date__gte=datetime.datetime.now())
        
        sent_users = set()  # Keep track of users who already received the message

        for session in active_sessions:
            session_data = session.get_decoded()
            user_id = session_data.get("user_id")

            if user_id and user_id not in sent_users:  # Check if user already received message
                try:
                    user = FormData.objects.get(id=user_id)

                    if user.phone:
                        phone_number = user.phone.strip()
                        if not phone_number.startswith("+"):
                            phone_number = f"+91{phone_number}"

                        client.messages.create(
                            from_=settings.TWILIO_WHATSAPP_NUMBER,
                            to=f"whatsapp:{phone_number}",
                            body=message
                        )
                        print(f"Message sent to {phone_number}: {message}")

                        sent_users.add(user_id)  # Mark user as messaged

                except FormData.DoesNotExist:
                    print(f"User with ID {user_id} not found.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Run at specific times
    scheduler.add_job(send_whatsapp_message, 'cron', hour=15, minute=23)
    scheduler.add_job(send_whatsapp_message, 'cron', hour=12, minute=0)
    scheduler.add_job(send_whatsapp_message, 'cron', hour=20, minute=2)
    
    scheduler.start()