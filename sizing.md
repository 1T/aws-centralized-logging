## Sizing the 1Ticket Centralized Logging ElasticSearch cluster

In July 2018, we observed that we logged about 25GB a day, and we had the requirement to keep the log data "hot" for about 3 weeks.

```
Disk storage needed

25GB x 18 days x 2 replica x 1.45 overhead factor = ~1.3TB
```

The [1.45 factor](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/sizing-domains.html) is operating system and Elastic Search overhead.

We selected an ES cluster configuration of: 

* 4 i3.large.elasticsearch data nodes (must be even number, to support having a replica in a different zone)
* 3 r4.large.elasticsearch master nodes (must be an odd number, 3 or 5)

The i3.large.elasticsearch instance has 475GB of storage, for a total of 1.8 TB for the 4 nodes.  We would have about 500 GB of free space.  The cost of the i3.large.elasticsearch instance is $0.163 per hour.  We bought 4 reserved instances, and the cluster as sized had been running smoothly.

## Resizing the Centralized Logging ES cluster to accomodate new services

Over time, we have been adding new services, and even configuring existing services like the DTI Portal (5GB per day) to log to ES.  Currently, we're logging about 72GB a day.  On 5/24, we experienced an outage due to the disk of one of the data nodes filling up.  

```
Disk storage needed

72GB x 18 days x 2 replica x 1.45 overhead factor = 3.8 TB
```

To support the new logging volume, we'll need 8 data nodes, which will give us 3.8 TB.  To reduce the storage required, we can reduce the number of retention days to 14 days, resulting in 3.0 TB required.
