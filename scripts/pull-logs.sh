#!/bin/bash

# usage:
# ./scripts/pull-logs.sh <dir-name>
remote_host=$1
remote_dir="membench-g5k"

rsync -aPv -e "ssh -p 22" "${remote_host}":${remote_dir}/logs .
