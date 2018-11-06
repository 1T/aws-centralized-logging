#!/usr/bin/env bash

awscurl --region us-east-1 --service es -X GET https://search-centralized-logging-ejzwewbtt2vlndvvji2orm55vu.us-east-1.es.amazonaws.com/_snapshot/snapshot-repository/_status
awscurl --region us-east-1 --service es -X GET https://search-centralized-logging-ejzwewbtt2vlndvvji2orm55vu.us-east-1.es.amazonaws.com/_snapshot/snapshot-repository/_all