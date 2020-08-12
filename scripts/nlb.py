import json
import socket
import boto3

print('Loading function')
# -- Set the following two parameters Or grab them from the environment --
myfailover = ['failover']
mySourceID = 'dev-mssql-rds'
RDSendpoint = "dev-mssql-rds.czefvc8cx8ou.us-east-1.rds.amazonaws.com"
tgtARN= 'arn:aws:elasticloadbalancing:us-east-1:356584979433:targetgroup/rds-networklb-target/5f75be617633dc52'


def lambda_handler(event, context):
    print (socket.gethostbyname(RDSendpoint))
    print("\nStart Lambda execution")

    # -- Set the following two parameters Or grab them from the environment --
    #myfailover = ['failover']
    #mySourceID = 'dev-mssql-rds'
    #RDSendpoint = "dev-mssql-rds.czefvc8cx8ou.us-east-1.rds.amazonaws.com"

    adict= {'version': '0', 'id': 'ffd1437c-e68f-2bea-cf0c-65d0c2e3c93e', 'detail-type': 'RDS DB Instance Event', 'source': 'aws.rds', 'account': '356584979433', 'time': '2020-08-11T20:31:02Z', 'region': 'us-east-1', 'resources': ['arn:aws:rds:us-east-1:356584979433:db:dev-mssql-rds'], 'detail': {'EventCategories': ['failover'], 'SourceType': 'DB_INSTANCE', 'SourceArn': 'arn:aws:rds:us-east-1:356584979433:db:dev-mssql-rds', 'Date': '2020-08-11T20:31:02.651Z', 'Message': 'Multi-AZ instance failover started. ', 'SourceIdentifier': 'dev-mssql-rds'}}

    #try-catch
    #try:

    if "detail" in adict:
        #print("found detail")
        if "EventCategories" in adict['detail']:
            #print("found Event categories")
            if adict['detail']['EventCategories'] == myfailover and adict['detail']['SourceIdentifier'] == mySourceID :
                print("Found a failover event of RDS")

                client = boto3.client('elbv2')
                response = client.register_targets(
                TargetGroupArn=tgtARN,
                Targets=[
                    {
                        'Id': socket.gethostbyname(RDSendpoint),
                        'Port': 1433,
                    },
                ]
                )
                #print(response)

    #except:
        #print("\nException raised")
        # send error to SNS topic

    print("\nEnd Lambda execution")
    #raise Exception('Something went wrong')



lambda_handler(" ", "context")
