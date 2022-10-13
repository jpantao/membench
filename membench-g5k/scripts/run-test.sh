#!/bin/bash

test_name=$1
n_runs=$2

cmake .
make clean
make

mkdir -p logs
log_file="logs/${test_name}.csv"
echo "run,node_type,access_type,throughput,cache_misses" | tee -a ${log_file}
for run in $(seq 1 ${n_runs}); do
  echo "------ run ${run} > ${log_file} ------"
  ./scripts/benchmark-node.sh 0 "dram" ${log_file} ${run}
  ./scripts/benchmark-node.sh 3 "pmem" ${log_file} ${run}
done