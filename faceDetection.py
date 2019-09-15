import time

import cv2
import paho.mqtt.client as mqtt

# initialize the capture device
cap = cv2.VideoCapture(1)
# initialize the classifier
face_cascade = cv2.CascadeClassifier(
    '/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'
    )

# initialize the broker
broker = "172.20.0.2"

def on_publish(client, message, result):
    print("message was published")

# initialize client
client = mqtt.Client("admin")
client.on_publish = on_publish
client.connect(broker)

# initialize a counter and define the total number of samples to send
counter = 0
samples = 10

# define a topic
topic = "faces"

while(counter < samples):
    # capture frame-by-frame
    _, frame = cap.read()

    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # for each detected face
    for (x, y, w, h) in faces:
        # create rectangle around it
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)

        # crop the ROI
        roi = gray[y:y+h, x:x+w]

        # encode as png, convert to bytes
        _, img = cv2.imencode('.png', roi)
        msg = img.tobytes()

        # publish the message
        client.publish(topic, msg, 0)

        # record that a face has been captured
        counter += 1

    # add a time buffer so the face image will be slightly more unique
    time.sleep(1)

# when everything done, release the capture
cap.release()
cv2.destroyAllWindows()
