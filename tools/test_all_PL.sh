#!/bin/bash

#/tools/test_all_PL.sh sherlock polish tests_automated

set_name=${1}
lang="polish"
src_dir="."
dest_dir=${2}

cd /data
process_dir()
{
  for filename in ${1}/*; do
    printf "Processing %s \n" "${filename}"
    filename_base=$(basename "${filename}")
    python /app/src/main.py conll-export "${lang}" "${filename}" "${2}/${filename_base}"
    printf "Done with %s \n" "${filename}"
  done
}

mkdir -p "/data/${dest_dir}/${set_name}"
process_dir "${src_dir}/${set_name}" "${dest_dir}/${set_name}"

echo "\n !DONE ALL! \n"
