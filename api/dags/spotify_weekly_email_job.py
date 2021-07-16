import smtplib
from email.message import EmailMessage

def spotify_weekly_email_function(subject, message, destination):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #This is where you would replace your password with the app password
    server.login('EMAIL@gmSERVERail.com', 'PASSWORD)')

    msg = EmailMessage()

    message = f'{message}\n'
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = 'me123@gmail.com'
    msg['To'] = destination
    server.send_message(msg)

spotify_weekly_email_function('Test subject', 'This is the message', 'RECEIVER@hotmail.com')