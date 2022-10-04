#!/bin/bash


test_name=$1
n_runs=$2

for run in $(seq 0 ${n_runs}); do
  dir="logs/${testname}/run_${run}"
  mkdir -p ${dir}
  echo "Starting run ${run}"
  ./scripts/bennchmark-node.sh 0 "dram" "${dir}/dram_benchmark.log"
  echo 'dram_benchmark'
  ./scripts/bennchmark-node.sh 3 "pmem" "${dir}/pmem_benchmark.log"
  echo 'pmem_benchmark'
done