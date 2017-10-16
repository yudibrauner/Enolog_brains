# # Import smtplib for the actual sending function
# import smtplib
#
# # Import the email modules we'll need
# from email.mime.text import MIMEText
#
# # Open a plain text file for reading.  For this example, assume that
# # the text file contains only ASCII characters.
# textfile = 'my_mail.txt'
# with open(textfile) as fp:
#     # Create a text/plain message
#     msg = MIMEText(fp.read())
#
# # me == the sender's email address
# # you == the recipient's email address
# msg['Subject'] = 'The contents of %s' % textfile
# msg['From'] = 'yudibrauner@gmail.com'
# msg['To'] = 'ybr@phaseone.com'
#
# # Send the message via our own SMTP server.
# s = smtplib.SMTP('localhost')
# s.send_message(msg)
# s.quit()

import smtplib


class MailHandler:

    def __init__(self, mail):
        self.recipient = mail

    def sendMail(self, msg):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        #Next, log in to the server
        server.login("smartwinery.ariel@gmail.com", "finalproject2017")
        #Send the mail
        server.sendmail("smartwinery.ariel.com", self.recipient, msg)
        server.close()

    # For setting the recipient=נמען
    def setRecipient(self, recipient):
        self.recipient = recipient