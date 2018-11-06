#!/usr/bin/env bash

awscurl --region us-east-1 --service es -X PUT https://search-centralized-logging-ejzwewbtt2vlndvvji2orm55vu.us-east-1.es.amazonaws.com/_snapshot/snapshot-repository/11-04-2018 -d'{
  "indices": ["cwl-2018.11.04","firehose-2018-11-04"],
  "ignore_unavailable": true,
  "include_global_state": false
}'