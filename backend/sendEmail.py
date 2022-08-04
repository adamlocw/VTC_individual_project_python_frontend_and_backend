import sendgrid
import os
from sendgrid.helpers.mail import *
from datetime import datetime
f = open("emailFrom.txt", "r")
emailFrom = f.readlines()[0]
f = open("sendGrid_API_Key.txt", "r")
sendGrid_API_Key = f.readlines()[0]


def sendEmail(emailTo, emailSubject, emailBody):
    sg = sendgrid.SendGridAPIClient(api_key=sendGrid_API_Key)
    from_email = Email(emailFrom)
    to_email = To(emailTo)
    subject = emailSubject
    content = Content("text/plain", emailBody)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


if __name__ == '__main__':
    emailTo = "adamlocw@gmail.com"
    emailSubject = "Hourly MACD trading of ETH."
    emailBody = f"ETH (MACD 12 26 9) SELL on Binance right now {datetime.now()}"
    sendEmail(emailTo, emailSubject, emailBody)
