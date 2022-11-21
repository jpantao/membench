#!/bin/bash

test_name=$1
n_runs=$2

cmake .
make clean
make

mkdir -p logs
log_file="logs/${test_name}.csv"
rm "${log_file}"

perf_event_list="cache-misses,L1-dcache-load-misses,L1-dcache-loads,LLC-load-misses,LLC-loads,LLC-store-misses,LLC-stores,l1d_pend_miss.pending,l1d_pend_miss.pending_cycles,l1d.replacement,l1d_pend_miss.fb_full,sw_prefetch_access.nta,sw_prefetch_access.prefetchw,sw_prefetch_access.t0,sw_prefetch_access.t1_t2,branch-misses,branches,cpu-cycles,instructions"

echo "starting test ${test_name} with ${n_runs} runs"

echo "run,node_kind,access_pattern,spinloop_iterations,throughput,$perf_event_list" | tee -a "${log_file}"
for run in $(seq 1 "${n_runs}"); do
  for w in $(seq 0 50 500); do
#    echo "------ run ${run} > ${log_file} ------"
    ./scripts/benchmark-node.sh 0 "dram" "${perf_event_list}" 0 "${w}" "${log_file}" "${run}"
    ./scripts/benchmark-node.sh 3 "pmem" "${perf_event_list}" 1 "${w}" "${log_file}" "${run}"
  done
done

echo "test ${test_name} finished"