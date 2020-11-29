#!/bin/bash

dockerize -wait tcp://neo_src:7687 -wait tcp://neo_dest:7687
if [ ${APP_MODE} = "graph-init" ]
then
  /app/pm2_setup.sh ${PM2_PROC_NUM}
  while true; do
    sleep 60
  done
elif [ ${APP_MODE} = "test" ]
then
  /app/start_test.sh
else
  cd /app/src
  python __init__.py
fi