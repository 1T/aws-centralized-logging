This Lambda cron job is configured to run at 4:00AM GMT to delete indices in the Centralized Logging Elastic Search instance.  The Lambda uses the Curator package to work with Elastic Search indices.
 
### Lambda inputs
 
The Lambda function expects the input event to contain these fields:

* AGE_KEY - delete indices older than this number of days.  Default is 21
* PREFIX_KEY = filter on indices whose name has this prefix.  Default is 'cwl-|firehose-'

*Example*

{'AGE_KEY':14, 'PREFIX_KEY':'cwl-|firehose-'}

By Elastic Search standard, the index name is expected to have a date suffix in the standard format of %Y-%m-%d or %Y.%m.%d

*Example*

* firehose-2018-08-28
* cwl-2018.09.30

### Serverless framework

This Lambda uses the [Serverless framework](https://www.google.com/search?q=serverless+framework&rlz=1C5CHFA_enUS801US801&oq=serverless+fra&aqs=chrome.0.0j69i60l3j69i59l2.4230j1j7&sourceid=chrome&ie=UTF-8) for deployment.  The serverless.yml file defines the Lambda function and other AWS resources needed.  The [Serverless Python Requirements plugin](https://www.npmjs.com/package/serverless-python-requirements) was used to manage vendored files.


### To do

1. Unit tests
2. Code formatting and linting
3. Run tests within Serverless framework