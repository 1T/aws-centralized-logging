#Alerting on DTI Portal slowness

The DTI Portal logs the duration of every user transaction.  The log is shipped to AWS Elastic Search, where we're able to build dashboards and monitor for Portal performance degradation.  However, AWS Kibana doesn't alert when the Portal becomes slow for a certain duration so that we can be warned .  As such, we need a Lambda that periodically polls Elastic Search, and writes a custom metric to Cloudwatch.  We can then create an Cloudwatch alarm that alerts when that metric is above a certain threhold for an evaluation period

## Elastic Search Query

The query below is used to query for transactions that take longer than 10 seconds

```
time_alive:/.*[1-9][1-9]\\..*/ AND _exists_:sql AND NOT sql:None
```

## Customer Cloudwatch Metric

The **slowportalalert** Lambda runs every 5 minutes, and writes a custom Cloudwatch metric with the value returned from the ElasticSearch query.  An alarm is raised if the metric, when measured every 5 minute over a half an hour period, adds up to above 15.  The aforementioned criteria are customizable, and will be adjusted as we learn to better identify when the Portal is becoming slow.

## Development

This Lambda was developed using the Serverless Framework.  See the **serverless.yml** file for the AWS resources set up, along with the Serverless plugins required to deploy the resources.