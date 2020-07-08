#!/bin/bash

default_capacity=100
default_interval=10
default_dest="/tmp/interviewTask"
capacity=$default_capacity
interval=$default_interval
dest="$default_dest"
content="A documentation is like a joke. If you have to explain it, it is not that good."


PARSED_ARGUMENT=$(getopt -q c:i:d: "$@")

echo "$@"

while [ -n "$1" ]; do
    case "$1" in
        -c) capacity="$2"
            shift ;;
        -i) interval="$2"
            shift ;;
        -d) dest="$2"
            shift ;;
        --) shift
            break ;;
        *) echo "$1 is not an option" ;;
    esac
    shift
done


function countFiles {
    count=$(ls -1 "$dest" | wc -l)
    echo $count 
}


if [ ! -d $dest ]; then
    echo "$dest does not exist or not a directory"
    mkdir "$dest"
    echo "Created $dest"
fi


count=$(countFiles)


while [ $count -lt $capacity ]; do
    d=$(date +"%S%M%H_%d-%m-%Y")
    next_file="$dest/$d" 
    if [ -f "$next_file" ]; then
        echo "[ERROR]: file $next_file has existed."
        return 1
    fi
    echo $content > "$next_file"
    count=$(countFiles)
    sleep $interval
done