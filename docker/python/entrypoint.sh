#!/bin/bash
cd /app
dockerize -wait tcp://neo_src:7687 -wait tcp://neo_dest:7687
mkdir ~/.ssh
echo "${SSH_PRIVATEKEY}" > ~/.ssh/id_rsa
echo "${SSH_PUBLICKEY}" > ~/.ssh/id_rsa.pub
chmod 700 ~/.ssh
chmod 644 ~/.ssh/id_rsa.pub
chmod 600 ~/.ssh/id_rsa
if [ "${APP_MODE}" = "graph-init" ]; then
  /app/pm2_setup.sh ${PM2_PROC_NUM}
fi
while true; do
  sleep 60
done
