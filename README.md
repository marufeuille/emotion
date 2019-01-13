# emotion
## What's this
My experimental implementation to use ML.
To analyze your face(photo) and send to Aliyun LogService in Realtime.

## How to use
### Dependency
#### ClientPC
- ClientPC is Mac Only, now.
- install software bellow
  - Python3
    - and ```pip3 install pika```
  - imagesnap (from homebrew,...)
  - docker
  - docker-compose

### Quickly use

### Environment Varialble
|Variable Name|Value to Set|
|:-----------|:-----------|
|FILE_DIR|Path to save Picture|
|MQ_HOST|Rabbit MQ's IP Addr or Hostname|
|QUEUE_NAME|Rabbit MQ's Queue Name|
