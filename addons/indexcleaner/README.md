
## Purging old indices

We purge old indices to free up storage in our Elastic Search cluster.  Indices older than a configurable number of days (default is 18) are automatically purged.

A Cloudwatch cron job is configured to run at 4:00AM GMT to invoke the Lambda IndexCleaner (**cleaner** function) to delete indices in the Centralized Logging Elastic Search instance.  The Lambda uses the Curator package to work with Elastic Search indices.
 
### Lambda inputs
 
The **cleaner** function expects the input event to contain these fields:

* AGE_KEY - delete indices older than this number of days.  Default is 21
* PREFIX_KEY = filter on indices whose name has this prefix.  Default is 'cwl-|firehose-'

*Example*

{'AGE_KEY':14, 'PREFIX_KEY':'cwl-|firehose-'}

By Elastic Search standard, the index name is expected to have a date suffix in the standard format of %Y-%m-%d or %Y.%m.%d

*Example*

* firehose-2018-08-28
* cwl-2018.09.30

## Creating snapshots of indices

We take a snapshot of the previous day's indices (e.g. firehose-yyyy-mm-dd, cwl-yyyy.mm.dd) and store in S3.

A Cloudwatch cron job is configured to run at 3:00AM GMT to invoke the Lambda IndexCleaner (**snapshot** function) to snapshot indices in the Centralized Logging Elastic Search instance to store in the S3 **1ticket-logging-archive** bucket.

### One time setup

To enable taking snapshots of Elastic Search indices to S3, we follow AWS's [recommendation](https://aws.amazon.com/blogs/database/use-amazon-s3-to-store-a-single-amazon-elasticsearch-service-index/).

```bash
cd indexcleaner/build
# create the role for ES to be able to read/write from S3
./create_snapshot_servicerole.sh
# create the ES repository where the snapshots metatadata will be stored
./create_snapshot_repo.sh
```

To run the create_snapshot_repo command, the user must have **Passrole** permission for the role created in create_snapshot_servicerole.  For example, see the esadmin user in the 1ticketlogging account.

## Serverless framework

This Lambda uses the [Serverless framework](https://www.google.com/search?q=serverless+framework&rlz=1C5CHFA_enUS801US801&oq=serverless+fra&aqs=chrome.0.0j69i60l3j69i59l2.4230j1j7&sourceid=chrome&ie=UTF-8) for deployment.  The serverless.yml file defines the Lambda function and other AWS resources needed.  The [Serverless Python Requirements plugin](https://www.npmjs.com/package/serverless-python-requirements) was used to manage vendored files.

### To do

1. Unit tests
2. Code formatting and linting
3. Run tests within Serverless framework
