
## Storing log entries into the ElasticSearch "infinity" index

Log entries stored in the Elastic Search (ES) **centralized-logging** domain are purged after a short period (e.g. 18 days).  However, we need to allow for searching of certain log entries, such as those related to Stubhub create listings, for a period of a year.

To allow for longer storage of certain log entries, the ES index **infinity** is used.  The entries in this index will be purged on a yearly basis.

## Stubhub Put and Post requests

We need to keep Stubhub Put and Post requests made by Shsyncx for a year.  These log entries relate to Stubhub requests that involve the creation and updates of listings.  Currently, Shsyncx logs to Cloudwatch, the content of that log group is then streamed to ES.  We won't disrupt that flow.  Instead, we have a lambda service that runs daily to *reindex* the Put and Post log entries into the infinity index for longer storage.

## Storage

The centralized-logging ES domain has 4 nodes, combining for 2TB of storage.  At the rate that we purge the centralized-logging domain, we expect to have about 800GB of free space on average at any time.

The Put and Post requests average about 600 MB a day, so we expect the infinity index to grow to about 190GB in a year.  That should still leave us with about 500GB of free space

## Kibana

Currently, there are 3 indices that can be searched in Kibana

* cwl-* : logging from all 1Ticket services except for Primary, going back 18 days
* firehose-* : logging from Primary Integration services, going back 18 days
* infinity : logging from Shsyncx Put and Post log entries, going back a year

We are in the process of combining the first two indices.

## Serverless framework

The **infinitylogging-prod-save_sh_putpost** Lambda uses the [Serverless framework](https://www.google.com/search?q=serverless+framework&rlz=1C5CHFA_enUS801US801&oq=serverless+fra&aqs=chrome.0.0j69i60l3j69i59l2.4230j1j7&sourceid=chrome&ie=UTF-8) for deployment.  The serverless.yml file defines the Lambda function and other AWS resources needed.  The [Serverless Python Requirements plugin](https://www.npmjs.com/package/serverless-python-requirements) was used to manage vendored files.

### To do

1. Unit tests
2. Code formatting and linting
3. Run tests within Serverless framework
