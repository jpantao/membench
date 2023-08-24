#!/bin/bash

test_name=$1
n_runs=$2
node=$(uniq "$OAR_NODE_FILE" | head -n 1)

./scripts/deploy.sh
echo "ssh \"${node}\" \"cd membench-g5k && ./scripts/membench-test.py ${test_name} -n ${n_runs}\""
ssh "${node}" "cd $(pwd) && ./scripts/membench-test.py ${test_name} -n ${n_runs}"
