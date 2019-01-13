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

#### Alibaba Cloud
- Activate LogService
- And Create LogProject and LogStore
- Create RAM Account(Optional, but strongly recommended)
- Create AccessKeyId and AccessKeySecret

### Quickly use
clone this repo.

```bash
git clone https://github.com/marufeuille/emotion
```

copy docker-compose-sample.yml to docker-compose.yml

```bash
cp docker-compose-sample.yml docker-compose.yml
```
and edit enviroment variable

```
      ALIYUN_ACCESSKEYID: "YOUR_ACCESSKEY_ID"
      ALIYUN_ACCESSKEYSECRET: "YOUR_SECRETKEY_ID"
      LOG_PROJECT: "YOUR_LOGPROJECT_NAME"
      LOG_LOGSTORE: "YOUR_LOGSTORE_NAME"
      LOG_TOPICS: "YOUR_TOPICS_NAME"
```

build image

```bash
docker-compose build
```

and run containers

```bash
docker-compose up
```

Congraturations!
Your Analysis and Send to LogService Enviroment is running.

Next setup take a photo regulary.

Complete this procedure, to run command bellow

```bash
cd cheese
bash index.sh
```
