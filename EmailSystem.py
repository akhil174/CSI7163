# https://docs.python.org/3.4/library/email.html#module-email
# https://www.mailtrap.io
# import essential libraries
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import base64
from LogSystem import logger


# method for sending the email to both the local server or mailtrap server(link above) depending on the flag
def sendEmail(filename, flag):
    if flag:
        # defining all the variables to contain required info
        portNumber = 465
        serverName = "smtp.mailtrap.io"
        username = "9ae404753f8e3e"
        password = "dcb5f31f0f986b"
        senderEmail = "admin@sleepdetect.com"
        receiverEmail = "user@sleepdetect.com"

        # creating an email object and adding details to it
        email = MIMEMultipart()
        email["Subject"] = "Sleepy Driver Alert!"
        email["From"] = senderEmail
        email["To"] = receiverEmail

        # encoding the image using base64 and adding it to the HTML body of the email
        encImage = base64.b64encode(open(filename, "rb").read()).decode()

        # HTML body of the image
        body = f"""\
        <html><body>
        <h4>Alert! The driver is feeling sleepy/drowsy. Please contact the driver ASAP to avoid any mishap. Thank 
        you.<br></h4> 
        <img src="data:image/jpg;base64,{encImage}">
        </body></html>"""

        textBody = MIMEText(body, "html")
        # attaching the HTML body to the email itself
        email.attach(textBody)

        # sending the email using smtplib and logging details
        try:
            with smtplib.SMTP(serverName, portNumber) as server:
                server.login(username, password)
                server.sendmail(senderEmail, receiverEmail, email.as_string())
            logger("Email with image has been sent successfully.")
            return
        except Exception as e:
            logger("An error occurred while sending the email -> " + str(e))
            return
    else:
        # this part uses the local SMTP server to send the email
        portNumber = "25"
        serverName = "smtp.sleepdetect.com"
        username = "admin"
        password = "admin"
        senderEmail = "system@sleepdetect.com"
        receiverEmail = "admin@sleepdetect.com"

        # creating an email object and adding details to it
        email = MIMEMultipart()
        email["Subject"] = "Sleepy Driver Alert!"
        email["From"] = senderEmail
        email["To"] = receiverEmail

        emailBody = MIMEText("Alert! The driver is feeling sleepy/drowsy. Please contact the driver ASAP to avoid any mishap. Thank you.")
        # attaching the email body to the email itself
        email.attach(emailBody)

        # adding the image and attaching it to the email object
        encImage = open(filename, "rb")
        emailImage = MIMEImage(encImage.read())
        email.attach(emailImage)
        encImage.close()

        # sending the email using smtplib and logging details
        server = smtplib.SMTP(serverName, portNumber)
        server.send_message(email, senderEmail, receiverEmail)
        logger("Email with image has been sent successfully.")
        return
