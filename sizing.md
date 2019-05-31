# Sizing the 1Ticket Centralized Logging ElasticSearch cluster

In July 2018, we observed that we logged about 25GB a day, and we had the requirement to keep the log data "hot" for about 3 weeks.

```
Disk storage needed

25GB x 18 days x 2 replica x 1.45 overhead factor = ~1.3TB
```

The [1.45 factor](https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/sizing-domains.html) is OS and ES overhead.

We selected an ES cluster configuration of: 

* 4 i3.large.elasticsearch data nodes (must be even number, to support having a replica in a different zone)
* 3 r4.large.elasticsearch master nodes (must be an odd number, 3 or 5)

The i3.large.elasticsearch instance has 475GB of storage, for a total of 1.8 TB for the 4 nodes.  We would have about 500 GB of free space.  The cost of the i3.large.elasticsearch instance is $0.163 per hour.  We bought 4 reserved instances, and the cluster as sized had been running smoothly
