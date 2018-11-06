#!/usr/bin/env bash

awscurl --region us-east-1 --service es -X POST 'https://search-centralized-logging-ejzwewbtt2vlndvvji2orm55vu.us-east-1.es.amazonaws.com/_snapshot/snapshot-repository' -d'{
    "type": "s3",
    "settings": {
        "bucket": "1ticket-logging-archive",
        "endpoint": "s3.amazonaws.com",
        "base_path": "archive/",
        "role_arn": "arn:aws:iam::405028608951:role/es-s3-repository"
    }
}'