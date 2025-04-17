import asyncio
import os
from email.message import EmailMessage
import smtplib

MAX_RETRIES = 3

async def send_email(subject, content):
    print("Sending email...")
    for attempt in range(MAX_RETRIES):
        try:
            email_from = os.getenv('EMAIL_FROM')
            email = EmailMessage()
            email['From'] = email_from
            email['To'] = os.getenv('EMAIL_TO')
            email['Subject'] = subject
            email.set_content(content)
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_from, os.getenv('EMAIL_TOKEN'))
                smtp.send_message(email)
                
            print("Email successfully sent")
            return True 
        except Exception as e:
            print (f"Attempt number {attempt + 1} to send alert failed")
            if attempt == MAX_RETRIES - 1:
                print(f"Error occurred while trying to send alert with the following:\nSubject:{subject}\nContent: {content}\nError: {e}")
                return False
            await asyncio.sleep(1)
