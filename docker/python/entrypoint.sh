#!/bin/bash
conda env create -f /app/environment.yml
conda activate disambiguation_graph
python -m spacy download en_core_web_sm
dockerize -wait tcp://neo_src:7687 -wait tcp://neo_dest:7687
/app/pm2_setup.sh ${PM2_PROC_NUM}
while true; do
  sleep 60
done
