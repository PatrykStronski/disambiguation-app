#!/bin/bash

number_of_workers=$1
nodes=8520962
batch=$((nodes/number_of_workers))
ind=0
strt=0
end=${batch}
until [ $ind -eq $((number_of_workers-1)) ]; do
  echo "${strt}  ${end}"
  strt=$((strt+batch))
  end=$((strt+batch))
  ind=$((ind+1))
done
end=$nodes
echo "${strt}  ${end}"
