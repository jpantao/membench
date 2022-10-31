#!/bin/bash

# usage:
# ./scripts/push-code.sh  <remote-host> 

remote_host=$1
remote_dir="membench-g5k"

make clean 

rm -rf $remote_dir
mkdir -p $remote_dir
cp -r ./scripts $remote_dir
cp membench.c $remote_dir
cp simplebench.c $remote_dir
cp CMakeLists.txt $remote_dir


rsync -aPv -e "ssh -p 22" $remote_dir "$remote_host":.