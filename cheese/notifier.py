import pika
import subprocess
from datetime import datetime

import os
import sys

MQ_HOST = "localhost" if os.environ.get('MQ_HOST') is None else os.environ.gey('MQ_HOST')
QUEUE_NAME = "PRE" if os.environ.get('QUEUE_NAME') is None else os.environ.get('QUEUE_NAME')

def send_to_mq(filename):
  connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
  channel = connection.channel()
  
  channel.queue_declare(queue=QUEUE_NAME)
  channel.basic_publish(exchange="",routing_key=QUEUE_NAME, body=filename)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Number of argment is exactly two.")
    print("Usage:")
    print("{} FILENAME".format(sys.argv[0]))
    exit(1)
  filename = sys.argv[1]
  send_to_mq(filename)
  exit(0)
