#!/bin/bash

filename=$1

records=$(cat "${filename}" | wc -l)
annotated=$(cat "${filename}" | grep s[0-9] | wc -l)
printf "Number of lines is: %d \n" ${records}
printf "Number of anntated lines is %d \n" ${annotated}
printf "The percentage is: %d percents\n" $((annotated*100/records))