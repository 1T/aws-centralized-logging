import boto3
import curator
import logging.config
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from indexcleaner import settings
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.config.dictConfig(settings.LOGGING_CONFIG)

AGE_KEY = 'AGE_KEY'
PREFIX_KEY = 'PREFIX_KEY'
SNAPSHOT_REPOSITORY = 'snapshot-repository'

LEVELS = {
    # Index prefix: age in days
    'cwl-|firehose-|portal-': 18,
    '90-day-': 90 
}


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


def filter(prefix, timestring, age):
    """Filter for indices older than X days."""

    ilo = curator.IndexList(es)

    ilo.filter_by_age(source='name', direction='older', timestring=timestring,
                          unit='days', unit_count=age)
    if ilo.working_list():
        ilo.filter_by_regex(kind='prefix', value=prefix)

    return ilo


def filter_yesterday():
    """Filter for indices with yesterdays date."""

    ilo = curator.IndexList(es)

    if ilo.working_list():
        yesterday = datetime.today() - timedelta(1)
        dateformat1 = yesterday.strftime('%Y-%m-%d')
        dateformat2 = yesterday.strftime('%Y\.%m\.%d')
        logger.info(f'^.*({dateformat1}|{dateformat2})')
        ilo.filter_by_regex(kind='regex', value=f'^.*({dateformat1}|{dateformat2})')

    return ilo


def snapshot(event, context):
    """Take a manual snapshot of indices from yesterday."""
    ilo = filter_yesterday()

    logger.info(f'Indices to snapshot: {ilo.working_list()}')

    if ilo.working_list():
        yesterday = datetime.today() - timedelta(1)
        name = yesterday.strftime('%m-%d-%Y')
        snapshot_indices = curator.Snapshot(ilo, repository=SNAPSHOT_REPOSITORY,
                                            name=name, wait_for_completion=False)
        snapshot_indices.do_action()
        logger.info(f'snapshot indices to {name}')


def cleaner(event, context):
    """Remove indices that are older than X days."""
    todo = LEVELS
    if event and AGE_KEY in event and PREFIX_KEY in event:
        todo = {event[PREFIX_KEY]: event[AGE_KEY]}

    for prefix, age in todo.items():
        ilo = filter(prefix, '%Y.%m.%d', age)

        logger.info(f'Indices to delete: {ilo.working_list()}')

        if ilo.working_list():
            delete_indices = curator.DeleteIndices(ilo)
            delete_indices.do_action()
            logger.info("Deleted indices")

        ilo = filter(prefix, '%Y-%m-%d', age)

        logger.info(f'Indices to delete: {ilo.working_list()}')

        if ilo.working_list():
            delete_indices = curator.DeleteIndices(ilo)
            delete_indices.do_action()
            logger.info("Deleted indices")
