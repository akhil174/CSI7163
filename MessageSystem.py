# https://www.textmagic.com/docs/api/
from textmagic.rest import TextmagicRestClient
from LogSystem import logger

# message to be displayed in the text message
msg = "Alert! The driver is feeling sleepy/drowsy. " \
      "Please contact the driver ASAP to avoid any mishap. Thank you."
# phone number of the person receiving the text message(can also accept list of phone numbers)
phoneNumber = "1"
# stores the message id
msgId = ""

def sendMessage():
    user_name = "manpreetsingh4"
    auth_token = "xu0eI43BVNlYWzBzHwsfP6Aa7gAphr"
    try:
        client = TextmagicRestClient(user_name, auth_token)
        message = client.messages.create(phones=phoneNumber, text=msg)
        msgId = message.messageId
    except Exception as e:
        logger("Some error occurred while sending the text message -> " + str(e))
        return
    if msgId != "":
        logger("Text message has been send successfully")
    else:
        logger("There was some error in sending the text message(No Exception caused)")
    return
