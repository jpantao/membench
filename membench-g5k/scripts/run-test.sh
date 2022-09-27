 #!/bin/bash

# usage:
# ./scripts/run-test.sh  <numa-node>

numa_node="$1"

mkdir -p logs

echo 'seq access'      
numactl --membind=$numa_node ./membench -s | tee logs/membench_seq.log
echo ''

echo 'seq access (prefetch)'      
numactl --membind=$numa_node ./membench -s -p | tee logs/membench_p_seq.log

echo ''
echo 'rand access'      
numactl --membind=$numa_node ./membench -r | tee logs/membench_rnd.log
echo ''

echo 'rand access (prefetch)'      
numactl --membind=$numa_node ./membench -r  -p| tee logs/membench_p_rnd.log

echo ''
echo 'pregen access'
numactl --membind=$numa_node ./membench -g | tee logs/membench_pgn.log
echo ''

echo 'pregen access (prefetch)'
numactl --membind=$numa_node ./membench -g -p | tee logs/membench_p_pgn.log
echo "#### FINISHED ####"