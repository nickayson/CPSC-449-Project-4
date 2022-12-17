#!/bin/sh
mkdir var
cd var
mkdir primary secondary third
cd primary
mkdir data mount
cd ..
cd secondary
mkdir data mount
cd ..
cd third
mkdir data mount
cd ..
mkdir rq_log
cd rq_log
touch rq_enqueue_log.txt