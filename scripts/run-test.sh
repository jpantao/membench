#!/bin/bash

test_name=$1
n_runs=$2

cmake .
make clean
make

mkdir -p logs
log_file="logs/${test_name}.csv"
rm "${log_file}"

echo "starting test ${test_name} with ${n_runs} runs"

echo "run,node_kind,access_pattern,spinloop_iterations,throughput,cache_misses" | tee -a "${log_file}"
for run in $(seq 1 "${n_runs}"); do
  for w in $(seq 0 50 500); do
#    echo "------ run ${run} > ${log_file} ------"
    ./scripts/benchmark-node.sh 0 "dram" "LLC-load-misses" 0 "${w}" "${log_file}" "${run}"
    ./scripts/benchmark-node.sh 3 "pmem" "LLC-load-misses" 1 "${w}" "${log_file}" "${run}"
  done
done

echo "test ${test_name} finished"