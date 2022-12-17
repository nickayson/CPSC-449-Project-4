#!/bin/sh
date 
rq requeue --all --queue default || echo "fail to requeue. will try again 10 mins later"
