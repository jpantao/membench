#!/bin/bash

# usage:
# ./scripts/benchmark-node.sh <numa_node> <node_type> <log_file> <run_n>

numa_node=$1
node_type=$2
perf_event=$3
cpu_node=$4
waitloop_iter=$5
log_file=$6
run_n=$7

function run_bench_2csv() {
    run_type=$1
    run_flag=$2
    prefetch_flag=$3
#    echo "numactl --membind="${numa_node}" --cpubind="${cpu_node}" perf record -e "${perf_event}" ./membench -c "${run_flag}" "${prefetch_flag}" -w "${waitloop_iter}" 2>/dev/null > tp"
    numactl --membind="${numa_node}" --cpubind="${cpu_node}" perf record -e "${perf_event}" ./membench -c "${run_flag}" "${prefetch_flag}" -w "${waitloop_iter}" 2>/dev/null > tp
    sleep 5
    perf report --header | grep -E Event | sed 's/^.*: //' > cm
    throughput=$(cat tp)
    cache_misses=$(cat cm)
    echo "${run_n},${node_type},${run_type},${waitloop_iter},${throughput},${cache_misses}" | tee -a "${log_file}"
    rm perf.data
}

#perf_event="cache-misses:u"

run_bench_2csv "seq" "-s"
run_bench_2csv "rnd" "-r"
run_bench_2csv "pgn" "-g"
run_bench_2csv "seq_prefetch" "-s" "-p"
run_bench_2csv "rnd_prefetch" "-r" "-p"
run_bench_2csv "pgn_prefetch" "-g" "-p"

rm tp
rm cm