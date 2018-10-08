import boto3
import curator
import logging.config
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from indexcleaner import settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.config.dictConfig(settings.LOGGING_CONFIG)

AGE_KEY = 'AGE_KEY'
AGE_DEFAULT_VALUE = 18
PREFIX_KEY = 'PREFIX_KEY'
PREFIX_DEFAULT_VALUE = 'cwl-|firehose-'

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, settings.AWS_REGION,
                   'es', session_token=credentials.token)


def filter(es, prefix, timestring, age):

    ilo = curator.IndexList(es)

    ilo.filter_by_age(source='name', direction='older', timestring=timestring,
                          unit='days', unit_count=age)
    if ilo.working_list():
        ilo.filter_by_regex(kind='prefix', value=prefix)

    return ilo

def cleaner(event, context):

    age = AGE_DEFAULT_VALUE
    prefix = PREFIX_DEFAULT_VALUE

    if event:
        if AGE_KEY in event:
            age = event[AGE_KEY]
        if PREFIX_KEY in event:
            prefix = event[PREFIX_KEY]

    es = Elasticsearch(
        hosts = [{'host': settings.ES_HOST, 'port': 443}],
        http_auth = awsauth,
        use_ssl = True,
        verify_certs = True,
        connection_class = RequestsHttpConnection
    )

    ilo = filter(es, prefix, '%Y.%m.%d', age)

    logger.info(f'Indices to delete: {ilo.working_list()}')

    if ilo.working_list():
        delete_indices = curator.DeleteIndices(ilo)
        delete_indices.do_dry_run()
        logger.info("Deleted indices")

    ilo = filter(es, prefix, '%Y-%m-%d', age)

    logger.info(f'Indices to delete: {ilo.working_list()}')

    if ilo.working_list():
        delete_indices = curator.DeleteIndices(ilo)
        delete_indices.do_dry_run()
        logger.info("Deleted indices")
