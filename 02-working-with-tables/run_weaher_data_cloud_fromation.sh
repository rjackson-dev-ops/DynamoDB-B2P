#!/bin/bash

aws cloudformation create-stack --stack-name  weather-station-table-cfn \
    --template-body file://weatherstationtable.json