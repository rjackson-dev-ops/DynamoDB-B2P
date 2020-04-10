#!/bin/bash

aws cloudformation create-stack --stack-name IDBucket  \
    --template-body file://IDBucket.json