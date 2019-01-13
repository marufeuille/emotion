import cv2 as cv
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

import pika

import sys
import os
from datetime import datetime
import time
import subprocess

cwd = os.path.dirname(os.path.abspath(__file__))

MQ_HOST = os.environ.get('MQ_HOST')
PRE_QUEUE_NAME = "PRE" if os.environ.get('PRE_QUEUE_NAME') is None else os.environ.get("PRE_QUEUE_NAME")
POST_QUEUE_NAME = "POST" if os.environ.get('POST_QUEUE_NAME') is None else os.environ.get("POST_QUEUE_NAME")
FILE_DIR = "/data" if os.environ.get('FILE_DIR') is None else os.environ.get("FILE_DIR")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST, heartbeat=0))
channel = connection.channel()
channel.queue_declare(queue=PRE_QUEUE_NAME)
channel.queue_declare(queue=POST_QUEUE_NAME)

face_cascade = cv.CascadeClassifier('/usr/local/lib/python3.5/site-packages/cv2/data/haarcascade_frontalface_default.xml')
model_path = '{}/trained_models/fer2013_big_XCEPTION.54-0.66.hdf5'.format(cwd)
emotions_classifier = load_model(model_path, compile=False)
emotion_target_size = emotions_classifier.input_shape[1:3]

def predict(filepath):
  img = cv.imread(filepath)
  gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  try:
    (x,y,w,h) = faces[0]
  except IndexError:
    sys.stderr.write('No face Found.')
    return None
  
  face_img = cv.resize(gray[y:y+h, x:x+w],(emotion_target_size)) / 255
  face_img = np.expand_dims(face_img, 0)
  face_img = np.expand_dims(face_img, -1)
  prediction = emotions_classifier.predict(face_img)[0]
  
  
  
  return"{},{},{},{},{},{},{}".format(prediction[0],prediction[1],prediction[2],prediction[3],prediction[4],prediction[5],prediction[6])
 

def callback(ch, method, properties, body):
  filename = body.decode("utf-8")
  print(" [x] Received %r" % (filename))
  filepath = "{}/{}.jpg".format(FILE_DIR,filename)
  result = predict(filepath)
  emotions = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
  if result is None:
    print("Result is Empty!!")
  else:
    print(result)
    recorded = datetime.strptime(filename,"%Y%m%d-%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

    channel.basic_publish(exchange="",routing_key=POST_QUEUE_NAME, body="{},{}".format(recorded,result))
  subprocess.call(["rm","-f",filepath])

channel.basic_consume(callback,queue=PRE_QUEUE_NAME,no_ack=True)
channel.start_consuming()
