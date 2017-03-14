#!/bin/bash
for file in test*.py; do
    echo $file;
    PREFIX=temp;
    if [[ $file[6,6] == "t" ]];
        then PREFIX=$file[6,10];
        else PREFIX=$file[6,11];
    fi
    FILENAME=$PREFIX.xml
    py.test -n 5 -v $file --junitxml=./results/$FILENAME;
    #break;
done
