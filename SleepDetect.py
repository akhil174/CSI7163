# importing required libraries
# used for computer vision
import cv2
# used for image processing
import imutils
# used for facial landmarks
import dlib
from scipy.spatial import distance
from imutils import face_utils
import threading
from MessageSystem import sendMessage
from LogSystem import logger
from EmailSystem import sendEmail
# for playing the alarm sound
import playsound

# defining the alarm file path
alarmFilePath = 'C:\\Users\\Admin\\PycharmProjects\\SleepDetect\\analog-alarm.mp3'
# defining the path for the pre-trained model for face recognition
predictFilePath = 'C:\\Users\\Admin\\PycharmProjects\\SleepDetect\\face_shape_landmarks_predictor.dat'


# method for sounding the alarm
def soundAlarm():
    # sound = vlc.MediaPlayer(alarmFilePath)
    # sound.play()
    playsound.playsound(alarmFilePath)


# method for capturing the image
def captureImage(image):
    cv2.imwrite(imageName, image)
    # sending the image to the email here
    # by default sends email to the mailtrap server
    sendEmail(imageName, True)


# method for calculating eye aspect ratio
def eyeAspectRatio(eye):
    # euclidean distance for vertical points of the eye
    vert1 = distance.euclidean(eye[1], eye[5])
    # euclidean distance for vertical points of the eye
    vert2 = distance.euclidean(eye[2], eye[4])
    # euclidean distance for horizontal point of the eye
    horz = distance.euclidean(eye[0], eye[3])

    EAR = (vert1 + vert2) / (2.0 * horz)
    return EAR


# threshold value(we considered) for the distance between the eyes to consider him drowsy/sleepy
earThreshold = 0.25
# number of frames for which we will check the earThreshold
frame_check = 16
# setting the alarm flag
alarm = False
# setting the default name for saving the image
imageName = "caught.jpg"

# loading the default face detector provided by dlib library
detector = dlib.get_frontal_face_detector()
logger("dlib face detector loaded")

# variable containing the prediction points
predict = dlib.shape_predictor(predictFilePath)

# storing the start and end for both the eyes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# starting up the camera(for now using laptop camera)
camera = cv2.VideoCapture(0)
logger("camera started...")

# flag for counting the number of frames the person has eyes closed
flag = 0

# initializing count for sending the text message
count = 0

while True:
    # reading the frame by frame video from the camera
    success, frame = camera.read()

    # setting the frame of the width to 500
    frame = imutils.resize(frame, width=550)

    # converting the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # converting the frame to LAB color space
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # getting the facial points from the detector
    subjects = detector(gray, 0)

    for subject in subjects:
        shape = predict(gray, subject)
        shape = face_utils.shape_to_np(shape)

        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = eyeAspectRatio(leftEye)
        rightEAR = eyeAspectRatio(rightEye)

        # storing the ratio average of the eyes
        EAR = (leftEAR + rightEAR) / 2.0
        # used opencv for for detecting the eye boundaries
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 1, 0, 0.1), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 1, 0, 0.1), 1)

        # if the eye aspect ratio is less than the threshold then the person is feeling sleepy
        if EAR < earThreshold:
            flag = flag + 1
            if flag >= frame_check:
                count = count + 1
                if count == 1:
                    captureImage(frame)
                    logger("Driver found sleepy, alert initiated")
                    logger("Sound played to alert the driver")
                    sendMessage()
                    alarm = True
                    # putting the method in the thread
                    thread = threading.Thread(target=soundAlarm)
                    # run the thread in the background
                    thread.daemon = True
                    thread.start()
        else:
            flag = 0
            alarm = False
        cv2.putText(frame, "Eye-Aspect-Ratio: {:.2f}".format(EAR), (250, 20),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 100, 200), 2)
    cv2.imshow("SleepDetect App", frame)
    if alarm:
        displayText = cv2.putText(frame, "Alert! Driver is sleepy", (125, 175), cv2.FONT_HERSHEY_COMPLEX, 1,
                                  (0, 100, 200), cv2.LINE_4, False)
        cv2.imshow("SleepDetect App", displayText)
    key = cv2.waitKey(1) & 0xFF
    # pressing 'c' on the keyword will close the app
    if key == ord("c"):
        logger("Camera stopped by the user")
        break
cv2.destroyAllWindows()
camera.release()
camera.stop()
soundAlarm().terminate()
