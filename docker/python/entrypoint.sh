#!/bin/bash
cd /app
dockerize -wait tcp://neo_src:7687 -wait tcp://neo_dest:7687
if [ "${APP_MODE}" = "graph-init" ]; then
  /app/pm2_setup.sh ${PM2_PROC_NUM}
fi
while true; do
  sleep 60
done
