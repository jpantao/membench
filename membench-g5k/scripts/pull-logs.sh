#!/bin/bash

# usage:
# ./scripts/pull-logs.sh <dir-name> <remote-host>

dir_name=$1
remote_host=$2

rsync -aPv -e "ssh -p 22" ${remote_host}:${dir_name}/logs .
