#!/bin/bash

test_name=$1
n_runs=$2

cmake .
make clean
make

mkdir -p logs
log_file="logs/${test_name}.csv"
rm ${log_file}

echo "run,node_type,access_type,waitloop_iter,throughput,cache_misses" | tee -a "${log_file}"

for run in $(seq 1 "${n_runs}"); do
  for w in $(seq 10 10 500); do
    echo "------ run ${run} > ${log_file} ------"
    ./scripts/benchmark-node.sh 0 "dram" "cache-misses:u" 0 "${w}" "${log_file}" "${run}"
    ./scripts/benchmark-node.sh 3 "pmem" "cache-misses:u" 1 "${w}" "${log_file}" "${run}"
  done
done
