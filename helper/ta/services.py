"""This module provides access functions to check against services that supports tagging"""

class Services:

    __Names = {
                    "AmazonEC2": "ec2", "AmazonS3": "s3", "AmazonVPC": "ec2", "AWSLambda":"lambda", 
		    "AmazonCloudWatch":"logs", "AmazonRDS":"rds", "AmazonES":"es", "ElasticMapReduce":"emr",
                    "AmazonDynamoDB":"dynamodb", "AmazonKinesisFirehose":"firehose", "AmazonGlacier":"glacier",
                    "awskms":"kms", "AmazonApiGateway":"apigateway", "AmazonKinesis":"kinesis",
		    "AWSCloudTrail":"cloudtrail", "AWSQueueService":"sqs", "AWSSecretsManager": "secretsmanager",
		    "AmazonCloudFront": "cloudfront", "AmazonEFS": "efs", "AmazonSageMaker": "sagemaker",
		    "AmazonRedshift": "redshift", "AmazonElastiCache": "elasticache",
		    "AmazonWorkSpaces": "workspaces", "AWSDirectoryService": "ds", "AmazonDAX": "dax",
		    "AmazonRoute53": "route53", "AWSDirecttConnect": "directconnect",
                    "datapipeline": "datapipeline"
                }

    def __init__(self):
        pass

    def GetB3ServiceName(self, Name):
        """Return the boto3 service name"""

        return Services.__Names[Name]

    def GetServices(self):
        """Return services as dictionary of CsvServiceName to B3ServiceName, i.e. AmazonApiGateway: apigateway"""

        return Services.__Names

def GetB3ServiceName(Name):
    """Return boto3 service name or None if it's not supported"""
    
    try:
        return Services().GetB3ServiceName(Name)
    except:
        return None

    return None

def GetServices():
    """Return services as dictionary, i.e. CsvServiceName:B3ServiceName"""

    return Services().GetServices()
