import boto3
import curator
import logging.config
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from infinity import settings
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.config.dictConfig(settings.LOGGING_CONFIG)

PREFIX_KEY = 'PREFIX_KEY'
PREFIX_DEFAULT_VALUE = 'cwl-'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, settings.AWS_REGION,
                   'es', session_token=credentials.token)
es = Elasticsearch(
    hosts=[{'host': settings.ES_HOST, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def filter_yesterday(prefix):
    ''' filter for indices with yesterdays date '''

    ilo = curator.IndexList(es)

    if ilo.working_list():
        yesterday = datetime.today() - timedelta(1)
        dateformat1 = yesterday.strftime('%Y-%m-%d')
        dateformat2 = yesterday.strftime('%Y\.%m\.%d')
        ilo.filter_by_regex(kind='regex', value=f'^.*({dateformat1}|{dateformat2})')

    if ilo.working_list():
        ilo.filter_by_regex(kind='prefix', value=prefix)

    return ilo


def save_stubhub_putpost_requests(event, context):
    ''' reindex entries to another index for longer storage '''

    prefix = PREFIX_DEFAULT_VALUE

    if event:
        if PREFIX_KEY in event:
            prefix = event[PREFIX_KEY]

    ilo = filter_yesterday(prefix)

    if ilo.working_list():

        yesterday = datetime.today() - timedelta(1)
        dateformat = yesterday.strftime('%Y-%m-%d')
        index_name = ilo.working_list()[0]
        from_date = dateformat + "T00:00:00"
        to_date = dateformat + "T23:59:59"
        logger.info(f'reindexing entries from index {index_name}, filtering from {from_date} to {to_date}')

        request_body = {
            "source": {
                "index": index_name,
                "query": {
                    "bool": {
                        "must": [
                            {
                                "query_string": {
                                    "query": "appname:shsyncx AND (message:\"POST https://api.stubhub.com\" OR message:\"PUT https://api.stubhub.com\")",
                                    "analyze_wildcard": True,
                                    "default_field": "*"
                                }
                            },
                            {
                                "range": {
                                    "@timestamp": {
                                        "gte": from_date,
                                        "lte": to_date
                                    }
                                }
                            }
                        ],
                        "filter": [],
                        "should": [],
                        "must_not": []
                    }
                }
            },
            "dest": {
                "index": "infinity"
            }
        }

        reindex = curator.Reindex(ilo,request_body=request_body,
                                  wait_for_completion=False)
        reindex.do_action()