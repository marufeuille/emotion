import pika

import sys
import os
import time

from aliyun.log.logitem import LogItem
from aliyun.log.logclient import LogClient
from aliyun.log.putlogsrequest import PutLogsRequest
from aliyun.log import LogException

MQ_HOST = os.environ.get('MQ_HOST')
QUEUE_NAME = "POST" if os.environ.get('QUEUE_NAME') is None else os.environ.get("QUEUE_NAME")
FILE_DIR = "/data" if os.environ.get('FILE_DIR') is None else os.environ.get("FILE_DIR")

LOG_ENDPOINT = "ap-northeast-1.log.aliyuncs.com" if os.environ.get("LOG_ENDPOINT") is None else os.environ.get("LOG_ENDPOINT")
ALIYUN_ACCESSKEYID = os.environ.get("ALIYUN_ACCESSKEYID")
ALIYUN_ACCESSKEYSECRET = os.environ.get("ALIYUN_ACCESSKEYSECRET")
LOG_PROJECT = os.environ.get("LOG_PROJECT")
LOG_LOGSTORE = os.environ.get("LOG_LOGSTORE")
LOG_TOPICS = "" if os.environ.get("LOG_TOPICS") is None else os.environ.get("LOG_TOPICS")
LOG_SOURCE = "" if os.environ.get("LOG_SOURCE") is None else os.environ.get("LOG_SOURCE")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST, heartbeat=0))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

client = LogClient(LOG_ENDPOINT, ALIYUN_ACCESSKEYID, ALIYUN_ACCESSKEYSECRET)
def callback(ch, method, properties, body):
  result = body.decode("utf-8")
  print(" [x] Received %r" % (result))
  emotions = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
  print(result)
  values = result.split(",");
  try:
    recorded = values.pop(0)

    print(recorded)
    logitem_list = []
    for i in range(len(emotions)):
      item = LogItem()
      contents = [
              ('emotion', emotions[i]),
              ('value', values[i]),
              ('recorded', recorded)
      ]
      print(contents)
      item.set_time(int(time.time()))
      item.set_contents(contents)
      logitem_list.append(item)

    req = PutLogsRequest(LOG_PROJECT, LOG_LOGSTORE, LOG_TOPICS, LOG_SOURCE, logitem_list)
    res = client.put_logs(req)
    res.log_print()
  except LogException:
    import traceback
    traceback.print_exc()
    channel.basic_publish(exchange="",routing_key=QUEUE_NAME, body=result)

channel.basic_consume(callback,queue=QUEUE_NAME,no_ack=True)
channel.start_consuming()

