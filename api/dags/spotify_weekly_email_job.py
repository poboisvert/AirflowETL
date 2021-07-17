import smtplib
from email.message import EmailMessage

def spotify_weekly_email_function():

    subject = 'Test subject'
    message = 'This is the message'
    destination = 'sender@gmail.com'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    #This is where you would replace your password with the app password - it's your gmail account (the sender account)
    server.login('receiver@gmail.com', 'email_password)')

    msg = EmailMessage()

    message = f'{message}\n'
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = 'me123@gmail.com'
    msg['To'] = destination
    server.send_message(msg)

if __name__ == '__main__':
    spotify_weekly_email_function('Test subject', 'This is the message', 'test@test.com')