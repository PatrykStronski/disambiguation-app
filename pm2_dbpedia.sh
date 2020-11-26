#!/bin/bash
cd ./src
number_of_workers=$1
nodes=6569091
strt=346000
batch=$(((nodes-strt)/number_of_workers))
ind=0
end=$((batch+strt))
until [ $ind -eq $((number_of_workers-1)) ]; do
  echo "${strt}  ${end}"
  pm2 start __init__.py --name "graph_creation${ind}" --no-autorestart -f -- "init-graph" "${strt}" "${end}"
  strt=$((strt+batch))
  end=$((strt+batch))
  ind=$((ind+1))
done
end=$nodes
echo "${strt}  ${end}"
pm2 start __init__.py --name "graph_creation${ind}" --no-autorestart -f -- "init-graph" "${strt}" "${end}"
