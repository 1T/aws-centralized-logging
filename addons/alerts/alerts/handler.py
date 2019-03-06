import boto3
import json
import requests
import logging.config
from requests_aws4auth import AWS4Auth
from alerts import settings
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.config.dictConfig(settings.LOGGING_CONFIG)

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, settings.AWS_REGION,
                   'es', session_token=credentials.token)
cloudwatch = boto3.client('cloudwatch')


def slowportalalert(event, context):

    current_time = int(1000.0*datetime.timestamp(datetime.now()))
    back_to = current_time - int(settings.SAMPLE_PERIOD)

    query = {
              "query": {
                "bool": {
                  "must": [
                    {
                      "query_string": {
                        "query": "time_alive:/.*[1-9][1-9]\\..*/ AND _exists_:sql AND NOT sql:None",
                        "analyze_wildcard": True,
                        "default_field": "*"
                      }
                    },
                    {
                      "range": {
                        "@timestamp": {
                          "gte": back_to,
                          "lte": current_time,
                          "format": "epoch_millis"
                        }
                      }
                    }
                  ],
                  "filter": [],
                  "should": [],
                  "must_not": []
                }
              }
            }

    headers = { "Content-Type": "application/json" }

    try:
        resp = requests.get(settings.ES_URL, auth=awsauth, headers=headers, data=json.dumps(query))
    except requests.exceptions.RequestException as e:
        logger.info(f'Failed to query ES {e}')
    else:
        if resp.status_code == 200:
            num_slow = resp.json()['count']
            logger.info(f'Num slow Portal transactions in last period {num_slow}')

            try:
                cloudwatch.put_metric_data(
                    MetricData=[
                        {
                            'MetricName': 'PORTAL_SLOW_TRANSACTIONS',
                            'Dimensions': [
                                {
                                    'Name': 'TRANSACTION',
                                    'Value': 'SLOW'
                                },
                            ],
                            'Unit': 'None',
                            'Value': num_slow
                        },
                    ],
                    Namespace='PERFORMANCE/PORTAL'
                )
            except Exception as e:
                logger.info(f'Failed to publish metric {e}')
        else:
            logger.error(f'Query to ES to retrieve slow Portal transactions failed {resp.status_code}')

