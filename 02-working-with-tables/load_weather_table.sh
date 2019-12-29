#!/bin/bash

# cat weatherstationtable.json  | jq '.Resources.table.Properties' > weatherstationtable_props.json
aws dynamodb create-table --cli-input-json file://weatherstationtable_props.json

# aws dynamodb describe-table --table-name=weatherstation_data