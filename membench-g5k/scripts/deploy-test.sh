#!/bin/bash


envrionment=$1
test_name=$2
n_runs=$3
node=$(uniq ${OAR_NODE_FILE} | head -n 1)

# kadeploy3 --no-kexec -a ${HOME}/public/kmem_dax_env.dsc -f ${OAR_NODE_FILE} -k
kadeploy3 -e debian11-x64-min -f $OAR_NODEFILE -k
ssh root@${node} 'apt update -y'
ssh root@${node} 'apt install -y cmake linux-perf'
ssh root@${node} 'echo "jantao  ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers'
# ssh root@${node} 'ndctl create-namespace --mode=devdax --map=mem'
# ssh root@${node} 'daxctl reconfigure-device dax1.0 --mode=system-ram'

ssh ${node} "cd $(pwd) && sudo ./scripts/run-test.sh ${test_name} ${n_runs}"

