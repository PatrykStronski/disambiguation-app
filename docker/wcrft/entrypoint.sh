#!/bin/bash
mkdir ~/.ssh
echo "${SSH_PUBLICKEY}" > ~/.ssh/authorized_keys
/etc/init.d/ssh start
while true; do
  sleep 60
done
