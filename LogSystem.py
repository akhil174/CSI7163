import os
import logging
from datetime import date

# initializing date variable to be used for log file name
today = date.today()
todayDate = today.strftime("%b-%d-%Y")
# file name for the log file
filename = 'log-' + str(todayDate) + '.log'
# creating the log file
open(filename, "a").close()


def logger(msg):
    # other approach for the log system
    # now = datetime.now()
    # currentTime = now.strftime("%H:%M:%S")
    # f = open(filename, "w+")
    # f.write(currentTime + " -> " + msg + "\r\n")
    # f.close()
    # opening the file in append mode to add the desired log msg
    logging.basicConfig(filename=filename, filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.warning(msg + "\r\n")
    return

