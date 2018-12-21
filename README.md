# The Problem

AWS exposes a rich and powerful set of APIs that can be used to manage tags. However, calling the raw APIs directly can be somewhat cumbersome.

Example 1: Update S3 bucket tag requires 12 lines of code

    Client = boto3.client('s3') 

    response = client.put_bucket_tagging(
        Bucket='string',
	Tagging={
	    'TagSet': [
	        {
	            'Key': 'string',
	            'Value': 'string'
	        },
	    ]
        }
    )

Example 2: Update Glacier tag requires 7 lines of code

    Client = boto3.client('glacier')

    response = client.add_tags_to_vault(
        vaultName='string',
        Tags={
            'string': 'string'
	}
    )

# The Solution

The APIs provided in this repository provides a much simpler way to interact with tags. It uses 1-2 lines instead of 7-12 to update tags for any service.

Example 1: Update S3 tag

    from aws.tag import UpdateTag

    UpdateTag('s3', ResourceId, TagName, TagValue)

Example 2: Update Glacier tag

    from aws.tag import UpdateTag

    UpdateTag('glacier', ResourceId, TagName, TagValue)

# The API Structure

This section describes the packages and modules that can be imported into your main script.

* helper/
  * aws/
    * **tag.py**: this module provides classes and functions. To make your program more compact, you can use functions instead of classes. Currently these functions are available: UpdateTag(), IsTagExists(), GetResources(), GetTagValues()
  * ta/
    * **services.py**: this module provides base classes and functions that maps service names from csv to boto3
    * **log.py**: this module provides logging

# The Main Scripts (Implementation Examples)

This section provides some example scripts that demonstrate how to use the simple API exposed via the modules.

**update-tags.py**: this script takes an input csv file with service and resource id columns with headers. Here is an example on how to invoke this script:

```
$ python update-tags.py --help

usage: update-tags.py [-h] [--overwrite yes|no] --tag AwsTag=CsvTag --csvfile filename

optional arguments:
  -h, --help           show this help message and exit
  --overwrite yes|no   yes to overwrite existing tag, and no will not overwrite
  --tag AwsTag=CsvTag  tag formatted as AwsTag=CsvTag, where AwsTag is the tag 
                       name in AWS, and CsvTag is the tag name in the csv file
  --csvfile filename   csv file
``` 

**missing-tags.py**: this script identifies missing tags for the services listed in services.py module.

# Services Tested
1. AmazonEC2
 * ec2
 * elb
 * elbv2
2. AWSLambda
3. AmazonDynamoDB
4. AmazonKinesisFirehose
5. AmazonKinesis
6. AmazonS3
7. AmazonElastiCache
8. AmazonRedshift
9. AmazonEFS
10. AmazonRDS
11. AmazonES
12. ElasticMapReduce
13. AmazonCloudWatch
14. awskms
