#!/bin/bash

PREFIX=${FILEDIR:-../pic}

if [ ! -d ${PREFIX} ]; then
  mkdir -p ${PREFIX}
fi

while :
do
  TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
  FILEPATH=${PREFIX}/${TIMESTAMP}.jpg
  imagesnap -w 1 ${FILEPATH} >/dev/null 2>&1
  python3 notifier.py ${TIMESTAMP}
  sleep 5
done
