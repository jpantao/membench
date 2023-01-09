#!/bin/bash

# usage:
# ./scripts/pull-logs.sh <dir-name> <remote-host>


remote_host=$1

rsync -aPv -e "ssh -p 12034" ${remote_host}:membench-g5k/figs .
