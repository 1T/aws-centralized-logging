from logging import INFO, ERROR
from os import getenv

ES_HOST = getenv('ES_HOST','search-centralized-logging-ejzwewbtt2vlndvvji2orm55vu.us-east-1.es.amazonaws.com')
ES_URL = 'https://' + ES_HOST + '/portal*/_count'

AWS_REGION = getenv('AWS_REGION','us-east-1')

SAMPLE_PERIOD = getenv('SAMPLE_PERIOD','300000')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'indexcleaner': {
            'level': INFO,
        },
        'curator': {
            'level': ERROR,
        },
        'elasticsearch': {
            'level': ERROR,
        }
    }
}