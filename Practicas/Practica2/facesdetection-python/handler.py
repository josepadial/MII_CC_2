import base64

import cv2
import numpy
import requests


def handle(req):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    img = requests.get(req).content
    image = numpy.frombuffer(img, numpy.uint8)
    img = cv2.imdecode(image, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
   
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    cv2.imwrite("image.png", img)

    with open("image.png", "rb") as f:
        image_final = base64.b64encode(f.read()).decode("utf-8")

    return f'<img src="data:image/jpeg;base64,{image_final}">'