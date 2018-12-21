"""This module provides classes and functions to update tags for AWS services"""
import boto3
from botocore.exceptions import ClientError

class TagNotSupportedError(Exception):
    """An exception class which can be raised when tagging not supported"""

    def __init__(self, Service):
        super().__init__('Tagging not supported for service ' + Service)


class InvalidEc2TypeError(Exception):
    """An exception class which can be raised for invalid ec2 type"""

    def __init__(self, ResourceId):
        super().__init__('Invalid ec2 type for ResourceId ' + ResourceId)

class AwsTag:
    """Update tags for supported AWS services"""

    __Services = ['ec2', 's3', 'lambda', 'logs', 'rds', 'es', 'emr', 'dynamodb', 'firehose', \
                     'glacier', 'kms', 'apigateway', 'kinesis', 'cloudtrail', 'sqs', 'secretsmanager', \
		     'cloudfront', 'efs', 'sagemaker', 'redshift', 'elasticache', 'workspaces', \
		     'ds', 'dax', 'route53', 'directconnect', 'datapipeline', 'elb', 'elbv2'
                    ]

    def __init__(self, Service=None, ResourceId=None):
        """Constructor"""

        self.Service = Service
        if self.Service not in AwsTag.__Services:
            raise TagNotSupportedError(str(self.Service))
        elif self.Service == 'ec2':
            try:
                ### get ec2 type such as elb, elb2 or ec2
                self.Service = self.GetEc2Type(ResourceId)
            except Exception as e:
                raise e


    def GetServiceName(self):
        """Return service name"""

        return self.Service


    def GetEc2Type(self, ResourceId):
        """Return type of ec2 such as elb, elbv2 or ec2"""
    
        if ResourceId != None and ResourceId.find('elasticloadbalancing') != -1:
            LbName = ResourceId.split(':')[-1].split('/')
            if len(LbName) == 2:
                return 'elb'
            elif len(LbName) == 4:
                return 'elbv2'
        elif self.Service == 'ec2':
            return 'ec2'
        else:
            raise InvalidEc2TypeError(ResourceId)


    def GetServicesCount(self):
        """Return number of supported services"""

        return len(AwsTag.__Services)


    def TagResource(self, ResourceId, TagName, TagValue):
        """Update tags using boto3 method tag_resource()"""

        Client = boto3.client(self.Service)

        if self.Service == 'lambda':
            response = Client.tag_resource (
                Resource = ResourceId,
		Tags =  {
                    TagName: TagValue
                }
	    )
        elif self.Service == 'dax':
            response = Client.tag_resource (
                ResourceName = ResourceId,
		Tags = [
		    {
                        'Key': TagName,
			'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'directconnect':
            response = Client.tag_resource (
                resourceArn = ResourceId,
		Tags = [
		    {
                        'key': TagName,
			'value': TagValue
		    }
		]
	    )
        elif self.Service == 'dynamodb':
            response = Client.tag_resource (
                ResourceArn = ResourceId,
		Tags = [
		    {
                        'Key': TagName,
			'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'kms':
            response = Client.tag_resource (
                KeyId = ResourceId,
		Tags = [
		    {
                        'TagKey': TagName,
			'TagValue': TagValue
		    }
		]
	    )
        elif self.Service == 'apigateway':
            response = Client.tag_resource (
                resourceArn = ResourceId,
		tags = [
		    {
			TagName: TagValue
		    }
		]
	    )
        elif self.Service == 'secretsmanager':
            response = Client.tag_resource (
                SecretId = ResourceId,
		Tags = [
		    {
			'Key': TagName,
			'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'cloudfront':
            response = Client.tag_resource (
                Resource = ResourceId,
		Tags = {
                    'Items': [
		        {
			    'Key': TagName,
			    'Value': TagValue
		        }
                    ]
		}
	    )
        else:
            raise TagNotSupportedError(str(self.Service))

        return True

    def AddTagsToResource(self, ResourceId, TagName, TagValue):
        """Update tags using boto3 method add_tags_to_resource()"""

        Client = boto3.client(self.Service)

        if self.Service == 'rds':
            response = Client.add_tags_to_resource (
                ResourceName = ResourceId,
                Tags = [
                    {
                        'Key': TagName,
                        'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'elasticache':
            response = Client.add_tags_to_resource (
                ResourceName = ResourceId,
                Tags = [
                    {
                        'Key': TagName,
                        'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'ds':
            response = Client.add_tags_to_resource (
                ResourceId = ResourceId,
                Tags = [
                    {
                        'Key': TagName,
                        'Value': TagValue
		    }
		]
	    )
        else:
            raise TagNotSupportedError(str(self.Service))

        return True

    def GetElbName(self, ResourceId):
        """Return elb name"""

        LbName = ResourceId.split(':')[-1].split('/')
        if ResourceId.find('elasticloadbalancing') != -1 and len(LbName) == 2:
            return LbName[-1]
        else:
            return None

    def GetSnapshotId(self, ResourceId):
        """Return snapshot id"""

        return ResourceId.split(':')[-1].split('/')[-1]

    def AddTags(self, ResourceId, TagName, TagValue):
        """Update tags using boto3 method add_tags()"""

        Client = boto3.client(self.Service)

        ### get sanitized resource id
        ResourceId = self.GetSanitizedResourceId(ResourceId)

        if self.Service == 'es':
            response = Client.add_tags (
                ARN = ResourceId,
                TagList = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'emr':
            response = Client.add_tags (
                ResourceId = ResourceId,
                Tags = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'cloudtrail':
            response = Client.add_tags (
                ResourceId = ResourceId,
                TagsList = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'sagemaker':
            response = Client.add_tags (
                ResourceArn = ResourceId,
                Tags = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'datapipeline':
            response = Client.add_tags (
                pipelineId = ResourceId,
                tags = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'elb':
            response = Client.add_tags (
                LoadBalancerNames = [ResourceId],
                Tags = [
	            {
                        'Key': TagName,
                        'Value': TagValue
	            }
                ]
	    )
        elif self.Service == 'elbv2':
            response = Client.add_tags (
                ResourceArns =  [ResourceId],
                Tags = [
	            {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        else:
            raise TagNotSupportedError(str(self.Service))

        return True


    def IsEc2Snapshot(self, ResourceId):
        """Return True if ec2 snapshot otherwise False"""

        if ResourceId.find('snapshot') != -1:
            return True
        else:
            return False


    def GetEc2ResourceId(self, ResourceId):
        """Return name or id of ec2 arn"""

        ### all ec2 resources (snapshots, internet gateway, nat gateway, etc...) uses id or name
        return ResourceId.split(':')[-1].split('/')[-1]

    def IsNatGateway(self, ResourceId):
        """Return True if nat gateway otherwise False"""

        if ResourceId.find('natgateway') != -1:
            return True
        else:
            return False

    def IsCustomerGateway(self, ResourceId):
        """Return True if customer gateway otherwise False"""

        if ResourceId.find('customer-gateway') != -1:
            return True
        else:
            return False

    def IsDedicatedHost(self, ResourceId):
        """Return True if dedicated host otherwise False"""

        if ResourceId.find('dedicated-host') != -1:
            return True
        else:
            return False

    def IsDhcpOptions(self, ResourceId):
        """Return True if dhcp options otherwise False"""

        if ResourceId.find('dhcp-options') != -1:
            return True
        else:
            return False

    def IsEgressIgw(self, ResourceId):
        """Return True if egress internet gateway otherwise False"""

        if ResourceId.find('egress-only-internet-gateway') != -1:
            return True
        else:
            return False

    def IsElasticGpu(self, ResourceId):
        """Return True if elastic gpu otherwise False"""

        if ResourceId.find('elastic-gpu') != -1:
            return True
        else:
            return False

    def IsEc2Image(self, ResourceId):
        """Return True if ec2 image otherwise False"""

        if ResourceId.find('image') != -1:
            return True
        else:
            return False

    def IsEc2Instance(self, ResourceId):
        """Return True if ec2 instance otherwise False"""

        if ResourceId.find('instance') != -1 and ResourceId.split(':')[-1].split('/')[0] == 'instance':
            return True
        else:
            return False

    def IsEc2InstanceProfile(self, ResourceId):
        """Return True if ec2 instance profile otherwise False"""

        if ResourceId.find('instance-profile') != -1:
            return True
        else:
            return False

    def IsInternetGateway(self, ResourceId):
        """Return True if internet gateway otherwise False"""

        if ResourceId.find('internet-gateway') != -1:
            return True
        else:
            return False

    def IsEc2KeyPair(self, ResourceId):
        """Return True if ec2 keypair otherwise False"""

        if ResourceId.find('key-pair') != -1:
            return True
        else:
            return False

    def IsLaunchTemplate(self, ResourceId):
        """Return True if launch template otherwise False"""

        if ResourceId.find('launch-template') != -1:
            return True
        else:
            return False

    def IsNacl(self, ResourceId):
        """Return True if network acl otherwise False"""

        if ResourceId.find('network-acl') != -1:
            return True
        else:
            return False

    def IsEni(self, ResourceId):
        """Return True if eni otherwise False"""

        if ResourceId.find('network-interface') != -1:
            return True
        else:
            return False

    def IsPlacementGroup(self, ResourceId):
        """Return True if placement group otherwise False"""

        if ResourceId.find('placement-group') != -1:
            return True
        else:
            return False

    def IsReservedInstance(self, ResourceId):
        """Return True if reserved instance otherwise False"""

        if ResourceId.find('reserved-instances') != -1:
            return True
        else:
            return False

    def IsRouteTable(self, ResourceId):
        """Return True if route table otherwise False"""

        if ResourceId.find('route-table') != -1:
            return True
        else:
            return False

    def IsSecurityGroup(self, ResourceId):
        """Return True if security group otherwise False"""

        if ResourceId.find('security-group') != -1:
            return True
        else:
            return False

    def IsSpotInstanceRequest(self, ResourceId):
        """Return True if spot instance request otherwise False"""

        if ResourceId.find('spot-instances-request') != -1:
            return True
        else:
            return False

    def IsSubnet(self, ResourceId):
        """Return True if subnet otherwise False"""

        if ResourceId.find('subnet') != -1:
            return True
        else:
            return False

    def IsEc2Volume(self, ResourceId):
        """Return True if ec2 volume otherwise False"""

        if ResourceId.find('volume') != -1:
            return True
        else:
            return False

    def IsVpc(self, ResourceId):
        """Return True if vpc otherwise False"""

        if ResourceId.find('vpc') != -1 and ResourceId.split(':')[-1].split('/')[0] == 'vpc':
            return True
        else:
            return False

    def IsVpcPeeringConnection(self, ResourceId):
        """Return True if vpc peering connection otherwise False"""

        if ResourceId.find('vpc-peering-connection') != -1:
            return True
        else:
            return False

    def IsVpnConnection(self, ResourceId):
        """Return True if vpn connection otherwise False"""

        if ResourceId.find('vpn-connection') != -1:
            return True
        else:
            return False

    def IsVpnGateway(self, ResourceId):
        """Return True if vpn gateway otherwise False"""

        if ResourceId.find('vpn-gateway') != -1:
            return True
        else:
            return False

    def CreateTags(self, ResourceId, TagName, TagValue):
        """Update tags using boto3 method create_tags()"""

        Client = boto3.client(self.Service)

        ### get sanitized resource id
        ResourceId = self.GetSanitizedResourceId(ResourceId)

        if self.Service == 'ec2':
            response = Client.create_tags(
                Resources = [
		    ResourceId
		],
		Tags = [
                    {
		        'Key': TagName,
		        'Value': TagValue
                    }
		]
	    )
        elif self.Service == 'efs':

            response = Client.create_tags(
                FileSystemId = ResourceId,
		Tags = [
                    {
		        'Key': TagName,
		        'Value': TagValue
                    }
		]
	    )
        elif self.Service == 'redshift':
            response = Client.create_tags(
                ResourceName = ResourceId,
		Tags = [
                    {
		        'Key': TagName,
		        'Value': TagValue
                    }
		]
	    )
        elif self.Service == 'workspaces':
            response = Client.create_tags(
                ResourceId = ResourceId,
		Tags = [
                    {
		        'Key': TagName,
		        'Value': TagValue
                    }
		]
	    )
        else:
            raise TagNotSupportedError(str(self.Service))

        return True

    def PutBucketTagging(self, ResourceId, TagName, TagValue):
        """Update s3 service tag"""
        Client = boto3.client('s3')

        ### get sanitized resource id
        ResourceId = self.GetSanitizedResourceId(ResourceId)

        response = {}
        try:
            response = Client.get_bucket_tagging (
                Bucket = ResourceId
	    )
        except Exception as e:
            if str(e).find('NoSuchTagSet') == -1:
                return False

        if 'TagSet' not in response:
            Tags = []
            Tags.append (
                {
                    'Key': TagName,
                    'Value': TagValue
                }
            )
        else:
            Tags = response['TagSet']

            ### if tag exists, replace tag value; otherwise, append tag
            if IsTagExists(self.Service, ResourceId, TagName):
                for Tag in Tags:
                    if Tag['Key'] == TagName:
                        Tag['Value'] = TagValue
            else:
                Tags.append (
                    {
                        'Key': TagName,
                        'Value': TagValue
                    }
                )
           
        response = Client.put_bucket_tagging (
            Bucket = ResourceId,
            Tagging = {
                'TagSet': Tags
	    }
        )


        return True

    def GetLogGroupName(self, ResourceId):
        """Return log group name"""

        return ResourceId.split(':')[-1]

    def TagLogGroup(self, ResourceId, TagName, TagValue):
        """Update cloudwatch logs service tag"""
        Client = boto3.client('logs')

        response = Client.tag_log_group(
            logGroupName = self.GetSanitizedResourceId(ResourceId),
            tags = {
	        TagName: TagValue
            }
	)

        return True

    def AddTagsToVault(self, ResourceId, TagName, TagValue):
        """Update glacier service tag"""
        Client = boto3.client('glacier')

        response = Client.add_tags_to_vault(
            vaultName = self.GetSanitizedResourceId(ResourceId),
            Tags = {
	            TagName: TagValue
            }
	)

        return True

    def AddTagsToStream(self, ResourceId, TagName, TagValue):
        """Update kinesis service tag"""
        Client = boto3.client('kinesis')

        response = Client.add_tags_to_stream(
            StreamName = self.GetSanitizedResourceId(ResourceId),
            Tags = {
	            TagName: TagValue
            }
	)

        return True

    def TagQueue(self, ResourceId, TagName, TagValue):
        """Update sqs service tag"""
        Client = boto3.client('sqs')

        response = Client.tag_queue(
            QueueUrl = self.GetSanitizedResourceId(ResourceId),
            Tags = [
                {
	            TagName: TagValue
                }
	    ]
	)

        return True

    def ChangeTagsForResource(self, ResourceId, TagName, TagValue):
        """Update route53 service tag"""

        Client = boto3.client('route53')

        response = Client.change_tags_for_resource ( 
            ResourceType = 'hostedzone',
            ResourceId = self.GetSanitizedResourceId(ResourceId),
            AddTags = [
	        {
		    'Key': TagName,
		    'Value': TagValue
		}
	    ]
	)

        return True

    def TagDeliveryStream(self, ResourceId, TagName, TagValue):
        """Update firehose service tag"""

        Client = boto3.client('firehose')

        response = Client.tag_delivery_stream(
	    DeliveryStreamName = self.GetSanitizedResourceId(ResourceId),
	    Tags = [
	        {
		    'Key': TagName,
		    'Value': TagValue
		}
	    ]
	)

        return True

    def UpdateTag(self, ResourceId, TagName, TagValue):
        """Calls other methods to update tags"""

        try:
            if self.Service == 'ec2':
                response = self.CreateTags(ResourceId, TagName, TagValue)
            elif self.Service == 'elb':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'elbv2':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 's3':
                response = self.PutBucketTagging(ResourceId, TagName, TagValue)
            elif self.Service == 'lambda':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'logs':
                response = self.TagLogGroup(ResourceId, TagName, TagValue)
            elif self.Service == 'rds':
                response = self.AddTagsToResource(ResourceId, TagName, TagValue)
            elif self.Service == 'es':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'emr':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'dynamodb':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'firehose':
                response = self.TagDeliveryStream(ResourceId, TagName, TagValue)
            elif self.Service == 'glacier':
                response = self.AddTagsToVault(ResourceId, TagName, TagValue)
            elif self.Service == 'kms':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'apigateway':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'kinesis':
                response = self.AddTagsToStream(ResourceId, TagName, TagValue)
            elif self.Service == 'cloudtrail':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'sqs':
                response = self.TagQueue(ResourceId, TagName, TagValue)
            elif self.Service == 'secretsmanager':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'cloudfront':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'efs':
                response = self.CreateTags(ResourceId, TagName, TagValue)
            elif self.Service == 'sagemaker':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'redshift':
                response = self.CreateTags(ResourceId, TagName, TagValue)
            elif self.Service == 'elasticache':
                response = self.AddTagsToResource(ResourceId, TagName, TagValue)
            elif self.Service == 'workspaces':
                response = self.CreateTags(ResourceId, TagName, TagValue)
            elif self.Service == 'ds':
                response = self.AddTagsToResource(ResourceId, TagName, TagValue)
            elif self.Service == 'dax':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'route53':
                response = self.ChangeTagsForResource(ResourceId, TagName, TagValue)
            elif self.Service == 'directconnect':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'datapipeline':
                response = self.AddTags(ResourceId, TagName, TagValue)
            else:
                raise TagNotSupportedError(self.Service)
        except Exception as e:
            raise e

        return True

    def GetSanitizedResourceId(self, ResourceId):
        """Return the sanitized resource id"""

        ### list services that does not required sanitization
        NotRequired = ['elbv2', 's3', 'lambda', 'rds', 'es', 'dynamodb', 'kms', 'apigateway', \
	               'cloudtrail', 'sqs', 'secretsmanager', 'cloudfront', 'sagemaker', 'redshift', \
		       'elasticache', 'workspaces', 'ds', 'dax', 'route53', 'directconnect', \
		       'datapipeline']
       
        try:
            if self.Service in NotRequired:
                return ResourceId
            elif self.Service == 'elb':
                return self.GetElbName(ResourceId)
            elif self.Service == 'ec2':
                return self.GetEc2ResourceId(ResourceId)
            elif self.Service == 'logs':
                return self.GetLogGroupName(ResourceId)
            elif self.Service == 'emr':
                return self.GetEmrClusterId(ResourceId)
            elif self.Service == 'firehose':
                return self.GetDeliveryStreamName(ResourceId)
            elif self.Service == 'glacier':
                return self.GetVaultName(ResourceId)
            elif self.Service == 'kinesis':
                return self.GetStreamName(ResourceId)
            elif self.Service == 'efs':
                return self.GetFileSystemId(ResourceId)
            else:
                raise TagNotSupportedError(self.Service)
        except Exception as e:
            raise e

        return ResourceId

    def GetFileSystemId(self, ResourceId):
        """Return efs filesystem id"""

        return ResourceId.split(':')[-1].split('/')[-1]

    def DescribeTags(self, ResourceId):
        """Get tags using boto3 method describe_tags()"""

        Client = boto3.client(self.Service) 

        ### get sanitized resource id
        ResourceId = self.GetSanitizedResourceId(ResourceId)
        
        if self.Service == 'elb':
            response = Client.describe_tags (
                LoadBalancerNames = [ResourceId]
	    )
        elif self.Service == 'elbv2':
            response = Client.describe_tags (
                ResourceArns = [ResourceId]
	    )
        elif self.Service == 'ec2':
            response = Client.describe_tags (
                Filters = [
	            {
                        'Name': 'resource-id',
	                'Values': [
	                    ResourceId
	                ]
		    }
	        ]
	    )
        elif self.Service == 'efs':

            response = Client.describe_tags (
                FileSystemId = ResourceId
	    )
        elif self.Service == 'redshift':
            response = Client.describe_tags (
                ResourceName = ResourceId
            )
        elif self.Service == 'workspaces':
            response = Client.describe_tags (
                ResourceId = ResourceId
            )
        elif self.Service == 'directconnect':
            response = Client.describe_tags (
                resourceArns = [
                    ResourceId
		]
            )
        else:
            raise TagNotSupportedError(self.Service)

        return response


    def GetBucketTagging(self, ResourceId):
        """Get tags using boto3 method get_bucket_tagging()"""
   
        Client = boto3.client('s3') 

        response = Client.get_bucket_tagging (
            Bucket = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def ListTags(self, ResourceId):
        """Get tags using boto3 method list_tags()"""
   
        Client = boto3.client(self.Service) 

        ### get sanitized resource id
        ResourceId = self.GetSanitizedResourceId(ResourceId)

        if self.Service == 's3':
            response = Client.list_tags (
                Bucket = ResourceId
	    )
        elif self.Service == 'es':
            response = Client.list_tags (
                ARN = ResourceId
	    )
        elif self.Service == 'cloudtrail':
            response = Client.list_tags (
                ResourceIdList = [
                    ResourceId
		]
	    )
        elif self.Service == 'sagemaker':
            response = Client.list_tags (
                ResourceArn = ResourceId
	    )
        elif self.Service == 'dax':
            response = Client.list_tags (
                ResourceName = ResourceId
	    )
        elif self.Service == 'lambda':
            response = Client.list_tags (
                Resource = ResourceId
	    )
        else:
            raise TagNotSupportedError(self.Service)
       
        return response

    def ListTagsLogGroup(self, ResourceId):
        """Get tags using boto3 method list_tags_log_group()"""
   
        Client = boto3.client('logs') 

        response = Client.list_tags_log_group (
            logGroupName = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def ListTagsForResource(self, ResourceId):
        """Get tags using boto3 method list_tags_for_resource()"""

        Client = boto3.client(self.Service) 
        
        ### get sanitized resource id
        ResourceId = self.GetSanitizedResourceId(ResourceId)

        if self.Service == 's3':
            response = Client.list_tags_for_resource (
                ResourceName = ResourceId
	    )
        elif self.Service == 'cloudfront':
            response = Client.list_tags_for_resource (
                Resource = ResourceId
	    )
        elif self.Service == 'elasticache':
            response = Client.list_tags_for_resource (
                ResourceName = ResourceId
            )
        elif self.Service == 'ds':
            response = Client.list_tags_for_resource (
                ResourceId = ResourceId
            )
        elif self.Service == 'route53':
            response = Client.list_tags_for_resource (
                ResourceType = 'hostedzone',
                ResourceId = ResourceId
            )
        elif self.Service == 'rds':
            response = Client.list_tags_for_resource (
                ResourceName = ResourceId
            )
        else:
            raise TagNotSupportedError(self.Service)

        return response


    def ListTagsOfResource(self, ResourceId):
        """Get tags using boto3 method list_tags_of_resource()"""

        Client = boto3.client('dynamodb')
        
        response = Client.list_tags_of_resource (
            ResourceArn = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def GetVaultName(self, ResourceId):
        """Return glacier vault name"""

        return ResourceId.split(':')[-1].split('/')[-1]

    def ListTagsForVault(self, ResourceId):
        """Get tags using boto3 method list_tags_for_vault()"""

        Client = boto3.client('glacier')

        response = Client.list_tags_for_vault (
            vaultName = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def ListResourceTags(self, ResourceId):
        """Get tags using boto3 method list_resource_tags()"""

        Client = boto3.client('kms')
        
        response = Client.list_resource_tags (
            KeyId = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def GetStreamName(self, ResourceId):
        """Return kinesis data stream name"""

        return ResourceId.split(':')[-1].split('/')[-1]

    def ListTagsForStream(self, ResourceId):
        """Get tags using boto3 method list_tags_for_stream()"""

        Client = boto3.client('kinesis')

        response = Client.list_tags_for_stream (
            StreamName = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def ListQueueTags(self, ResourceId):
        """Get tags using boto3 method list_queue_tags()"""

        Client = boto3.client('sqs')
        
        response = Client.list_queue_tags (
            QueueUrl = self.GetSanitizedResourceId(ResourceId)
	)

        return response

    def GetDeliveryStreamName(self, ResourceId):
        """Return firehose delivery stream name"""

        return ResourceId.split(':')[-1].split('/')[-1]

    def ListTagsForDeliveryStream(self, ResourceId):
        """Get tags using boto3 method list_tags_for_delivery_stream()"""

        Client = boto3.client('firehose')

        response = Client.list_tags_for_delivery_stream (
            DeliveryStreamName = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def DescribeSecret(self, ResourceId):
        """Get tags using boto3 method describe_secret()"""

        Client = boto3.client('secretsmanager')
        
        response = Client.describe_secret (
            SecretId = self.GetSanitizedResourceId(ResourceId)
	)

        return response

    def GetEmrClusterId(self, ResourceId):
        """Return emr cluster id"""

        return ResourceId.split(':')[-1].split('/')[-1]


    def DescribeCluster(self, ResourceId):
        """Get tags using boto3 method describe_cluster()"""

        Client = boto3.client('emr')
        
        response = Client.describe_cluster (
            ClusterId = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def DescribePipelines(self, ResourceId):
        """Get tags using boto3 method describe_pipelines()"""

        Client = boto3.client('datapipeline')
        
        response = Client.describe_cluster (
            pipelineIds = [
                self.GetSanitizedResourceId(ResourceId)
            ]
	)

        return response


    def GetTags(self, ResourceId):
        """Get tags using boto3 method get_tags()"""

        Client = boto3.client('apigateway')
        
        response = Client.get_tags (
            resourceArn = self.GetSanitizedResourceId(ResourceId)
	)

        return response


    def IsTagExists(self, ResourceId, TagName):
        """Calls other methods to check if tag exists"""

        try:
            if self.Service == 'elb' or self.Service == 'elbv2':
                response = self.DescribeTags(ResourceId)
                return True if len(list(filter(lambda TagKey: TagKey == TagName , [Tag['Key'] for Tag in [TD['Tags'] for TD in response['TagDescriptions']][0]]))) == 1 else False
            elif self.Service == 'ec2':
                response = self.DescribeTags(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 's3':
                response = self.GetBucketTagging(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['TagSet']])) else False
            elif self.Service == 'lambda':
                response = self.ListTags(ResourceId)
                return True if TagName in [x for x in response['Tags']] else False
            elif self.Service == 'logs':
                response = self.ListTagsLogGroup(ResourceId)
                return True if TagName in [x for x in response['tags']] else False
            elif self.Service == 'rds':
                response = self.ListTagsForResource(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['TagList']])) else False
            elif self.Service == 'es':
                response = self.ListTags(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['TagList']])) else False
            elif self.Service == 'emr':
                response = self.DescribeCluster(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [Tag for Tag in response['Cluster']['Tags']])) else False
            elif self.Service == 'dynamodb':
                response = self.ListTagsOfResource(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'firehose':
                response = self.ListTagsForDeliveryStream(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'glacier':
                response = self.ListTagsForVault(ResourceId)
                return True if TagName in [x for x in response['Tags']] else False
            elif self.Service == 'kms':
                response = self.ListResourceTags(ResourceId)
                return True if TagName in list(map(lambda x: x['TagKey'], [x for x in response['Tags']])) else False
            elif self.Service == 'apigateway':
                response = self.GetTags(ResourceId)
                return True if len([x for x in response['tags'] if x == TagName]) == 1 else False
            elif self.Service == 'kinesis':
                response = self.ListTagsForStream(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'cloudtrail':
                response = self.ListTags(ResourceId)
                return True if len(list(filter(lambda TagKey: TagKey == TagName , [Tag['Key'] for Tag in [TD['TagsList'] for TD in response['ResourceTagList']][0]]))) == 1 else False
            elif self.Service == 'sqs':
                response = self.ListTags(ResourceId)
                return True if TagName in [x for x in response['Tags']] else False
            elif self.Service == 'secretsmanager':
                response = self.DescribeSecret(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'cloudfront':
                response = self.ListTagsForResource(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'efs':
                response = self.DescribeTags(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'sagemaker':
                response = self.ListTags(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'redshift':
                response = self.DescribeTags(ResourceId)
                return True if TagName in [Tag['Key'] for Tag in [TR['Tag'] for TR in response['TaggedResources']]] else False
            elif self.Service == 'elasticache':
                response = self.ListTagsForResource(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['TagList']])) else False
            elif self.Service == 'workspaces':
                response = self.DescribeTags(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'ds':
                response = self.ListTagsForResource(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'dax':
                response = self.ListTags(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'route53':
                response = self.ListTagsForResource(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'directconnect':
                response = self.DescribeTags(ResourceId)
                return True if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])) else False
            elif self.Service == 'datapipeline':
                response = self.DescribePipelines(ResourceId)
                return True if TagName in [Tag['key'] for Tag in [PD['tags'] for PD in response['pipelineDescriptionList']][0]] else False
            else:
                raise TagNotSupportedError(self.Service)
        except Exception as e:
            raise e

        return False

    def GetTagValues(self, ResourceId, TagNames):
        """Get tag value corresponding to tag name for resource"""

        try:
            if self.Service == 'ec2':
                response = self.DescribeTags(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 's3':
                response = self.GetBucketTagging(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['TagSet'] if Tag['Key'] in TagNames]
            elif self.Service == 'lambda':
                response = self.ListTags(ResourceId)
                return [{K: V} for K,V in response['Tags'] if K in TagNames]
            elif self.Service == 'logs':
                response = self.ListTagsLogGroup(ResourceId)
                return [{K: V} for K,V in response['tags'] if K in TagNames]
            elif self.Service == 'rds':
                response = self.ListTagsForResource(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['TagList'] if Tag['Key'] in TagNames]
            elif self.Service == 'es':
                response = self.ListTags(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['TagList'] if Tag['Key'] in TagNames]
            elif self.Service == 'emr':
                response = self.DescribeCluster(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Cluster']['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'dynamodb':
                response = self.ListTagsOfResource(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'firehose':
                response = self.ListTagsForDeliveryStream(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'glacier':
                response = self.ListTagsForVault(ResourceId)
                return [{K: V} for K,V in response['Tags'] if K in TagNames]
            elif self.Service == 'kms':
                response = self.ListResourceTags(ResourceId)
                return [{Tag['TagKey']: Tag['TagValue']} for Tag in response['Tags'] if Tag['TagKey'] in TagNames]
            elif self.Service == 'apigateway':
                response = self.GetTags(ResourceId)
                return [{K: V} for K,V in response['tags'] if K in TagNames]
            elif self.Service == 'kinesis':
                response = self.ListTagsForStream(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'cloudtrail':
                response = self.ListTags(ResourceId)
                TagsList = map(lambda RTL: RTL['TagsList'], [RTL for RTL in response['ResourceTagList']])
                return [{Tag['Key']: Tag['Value']} for Tag in TagsList if Tag['Key'] in TagNames]
            elif self.Service == 'sqs':
                response = self.ListTags(ResourceId)
                return [{K: V} for K,V in response['Tags'] if K in TagNames]
            elif self.Service == 'secretsmanager':
                response = self.DescribeSecret(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'cloudfront':
                response = self.ListTagsForResource(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'efs':
                response = self.DescribeTags(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'sagemaker':
                response = self.ListTags(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'redshift':
                response = self.DescribeTags(ResourceId)
                Tags = [Tag['Tag'] for Tag in response['TaggedResources']]
                return [{Tag['Key']: Tag['Value']} for Tag in Tags if Tag['Key'] in TagNames]
            elif self.Service == 'elasticache':
                response = self.ListTagsForResource(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['TagList'] if Tag['Key'] in TagNames]
            elif self.Service == 'workspaces':
                response = self.DescribeTags(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'ds':
                response = self.ListTagsForResource(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'dax':
                response = self.ListTags(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'route53':
                response = self.ListTagsForResource(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'directconnect':
                response = self.DescribeTags(ResourceId)
                return [{Tag['Key']: Tag['Value']} for Tag in response['Tags'] if Tag['Key'] in TagNames]
            elif self.Service == 'datapipeline':
                response = self.DescribePipelines(ResourceId)
                Tags = list(map(lambda x: x['tags'], [tags for tags in response['pipelineDescriptionList']]))
                return [{Tag['Key']: Tag['Value']} for Tag in Tags if Tag['Key'] in TagNames]
            else:
                raise TagNotSupportedError(self.Service)
        except Exception as e:
            raise e

        return []


    def ListBuckets(self):
        """Return S3 buckets"""

        Client = boto3.client(self.Service)
        response = Client.list_buckets()
        return response


    def ListFunctions(self):
        """Return lambda functions"""

        Client = boto3.client(self.Service)
        response = Client.list_functions(
            MasterRegion = 'ALL',
            FunctionVersion = 'ALL'
	)
        return response


    def DescribeLogGroups(self):
        """Return cloudwatch logs"""

        Client = boto3.client(self.Service)
        return Client.describe_log_groups()


    def DescribeDbInstances(self):
        """Return rds instances"""

        Client = boto3.client(self.Service)
        return Client.describe_db_instances()


    def ListDomainNames(self):
        """Return elastic search domain names"""

        Client = boto3.client(self.Service)
        return Client.list_domain_names()

    
    def DescribeElasticSearchDomains(self, DomainNames):
        """Return elastic search domain arn"""

        Client = boto3.client(self.Service)
        return Client.describe_elasticsearch_domains(
            DomainNames = DomainNames
	)


    def ListClusters(self):
        """Return emr clusters id"""

        Client = boto3.client(self.Service)
        return Client.list_clusters()

    def ListTables(self):
        """Return dynamodb tables"""

        Client = boto3.client(self.Service)
        return Client.list_tables()

    def ListDeliveryStreams(self):
        """Return firehose delivery streams"""

        Client = boto3.client(self.Service)
        return Client.list_delivery_streams()

    def ListVaults(self):
        """Return vaults"""

        Client = boto3.client(self.Service)
        return Client.list_vaults()

    def ListKeys(self):
        """Return kms keys"""

        Client = boto3.client(self.Service)
        return Client.list_keys()

    def GetRestApis(self):
        """Return api gateway rest api"""

        Client = boto3.client(self.Service)
        return Client.get_rest_apis()

    def ListStreams(self):
        """Return kinesis streams"""

        Client = boto3.client(self.Service)
        return Client.list_streams()

    def DescribeTrails(self):
        """Return cloudtrail"""

        Client = boto3.client(self.Service)
        return Client.describe_trails()

    def ListQueues(self):
        """Return sqs"""

        Client = boto3.client(self.Service)
        return Client.list_queues()

    def ListSecrets(self):
        """Return secrets manager"""

        Client = boto3.client(self.Service)
        return Client.list_secrets()

    def ListDistributions(self):
        """Return cloudfront distributions"""

        Client = boto3.client(self.Service)
        return Client.list_distributions()

    def DescribeFileSystems(self):
        """Return efs"""

        Client = boto3.client(self.Service)
        return Client.describe_file_systems()

    def ListNotebookInstances(self):
        """Return sagemaker notebook instances"""

        Client = boto3.client(self.Service)
        return Client.list_notebook_instances()

    def DescribeClusters(self):
        """Return resources using boto3 describe_clusters()"""

        Client = boto3.client(self.Service)

        if self.Service == 'redshift':
            response = Client.describe_clusters() 
        elif self.Service == 'dax':
            response = Client.describe_clusters() 
        else:
            raise TagNotSupportedError(self.Service)

        return response

    def DescribeCacheClusters(self):
        """Return elasticache clusters"""

        Client = boto3.client(self.Service)
        return Client.describe_cache_clusters()

    def DescribeWorkspaces(self):
        """Return workspaces"""

        Client = boto3.client(self.Service)
        return Client.describe_workspaces()

    def DescribeDirectories(self):
        """Return directory services"""

        Client = boto3.client(self.Service)
        return Client.describe_directories()

    def ListHostedZones(self):
        """Return hosted zones"""

        Client = boto3.client(self.Service)
        return Client.list_hosted_zones()

    def DescribeVirtualInterfaces(self):
        """Return direct connect vifs"""

        Client = boto3.client(self.Service)
        return Client.describe_virtual_interfaces()

    def ListPipelines(self):
        """Return datapipelines"""

        Client = boto3.client(self.Service)
        return Client.list_pipelines()

    def GetEc2Resources(self):
        """Return list of ec2 resources"""

        Resources = []
        Client = boto3.client('ec2')

        ### get snapshots
        response = Client.describe_snapshots(
	)
        Resources += [R['SnapshotId'] for R in response['Snapshots']]

        ### get nat gateways
        response = Client.describe_nat_gateways(
	)
        Resources += [R['NatGatewayId'] for R in response['NatGateways']]

        ### get customer gateways
        response = Client.describe_customer_gateways(
	)
        Resources += [R['CustomerGatewayId'] for R in response['CustomerGateways']]

        ### get dedicated hosts
        response = Client.describe_hosts(
	)
        Resources += [R['HostId'] for R in response['Hosts']]

        ### get dedicated hosts
        response = Client.describe_hosts(
	)
        Resources += [R['HostId'] for R in response['Hosts']]

        ### get dhcp options
        response = Client.describe_dhcp_options(
	)
        Resources += [R['DhcpOptionsId'] for R in response['DhcpOptions']]

        ### get egress internet gateways
        response = Client.describe_egress_only_internet_gateways(
	)
        Resources += [R['EgressOnlyInternetGatewayId'] for R in response['EgressOnlyInternetGateways']]

        ### get egress internet gateways
        response = Client.describe_egress_only_internet_gateways(
	)
        Resources += [R['EgressOnlyInternetGatewayId'] for R in response['EgressOnlyInternetGateways']]

        ### get elastic gpus
        response = Client.describe_elastic_gpus(
	)
        Resources += [R['ElasticGpuId'] for R in response['ElasticGpuSet']]

        ### get ec2 images
        response = Client.describe_images(
	)
        Resources += [R['ImageId'] for R in response['Images']]

        ### get ec2 instances
        response = Client.describe_instances(
	)
        Resources += [InstanceId for InstanceId in [[J['InstanceId'] for J in I ]for I in [R['Instances'] for R in response['Reservations']]][0]]

        ### get ec2 instance profiles from instance profile associations
        response = Client.describe_iam_instance_profile_associations(
	)
        Resources += [R['IamInstanceProfile']['Id'] for R in response['IamInstanceProfileAssociations']]

        ### get internet gateways
        response = Client.describe_internet_gateways(
	)
        Resources += [R['InternetGatewayId'] for R in response['InternetGateways']]

        ### get ec2 key pairs
        response = Client.describe_key_pairs(
	)
        Resources += [R['KeyName'] for R in response['KeyPairs']]

        ### get launch templates
        response = Client.describe_launch_templates(
	)
        Resources += [R['LaunchTemplateId'] for R in response['LaunchTemplates']]

        ### get nacls
        response = Client.describe_network_acls(
	)
        Resources += [R['NetworkAclId'] for R in response['NetworkAcls']]

        ### get enis
        response = Client.describe_network_interfaces(
	)
        Resources += [R['NetworkInterfaceId'] for R in response['NetworkInterfaces']]

        ### get placement groups
        response = Client.describe_placement_groups(
	)
        Resources += [R['GroupName'] for R in response['PlacementGroups']]

        ### get reserved instances
        response = Client.describe_reserved_instances(
	)
        Resources += [R['ReservedInstancesId'] for R in response['ReservedInstances']]

        ### get route tables
        response = Client.describe_route_tables(
	)
        Resources += [R['RouteTablesId'] for R in response['RouteTables']]

        ### get security groups
        response = Client.describe_security_groups(
	)
        Resources += [R['GroupId'] for R in response['SecurityGroups']]

        ### get spot instance requests
        response = Client.describe_spot_instance_requests(
	)
        Resources += [R['SpotInstanceRequestId'] for R in response['SpotInstanceRequests']]

        ### get subnets
        response = Client.describe_subnets(
	)
        Resources += [R['SubnetId'] for R in response['Subnets']]

        ### get ec2 volumes
        response = Client.describe_volumes(
	)
        Resources += [R['VolumeId'] for R in response['Volumes']]

        ### get ec2 volumes
        response = Client.describe_volumes(
	)
        Resources += [R['VolumeId'] for R in response['Volumes']]

        ### get vpcs
        response = Client.describe_vpcs(
	)
        Resources += [R['VpcId'] for R in response['Vpcs']]

        ### get vpc peering connections
        response = Client.describe_vpc_peering_connections(
	)
        Resources += [R['VpcPeeringConnectionId'] for R in response['VpcPeeringConnections']]

        ### get vpc peering connections
        response = Client.describe_vpc_peering_connections(
	)
        Resources += [R['VpcPeeringConnectionId'] for R in response['VpcPeeringConnections']]

        ### get vpn connections
        response = Client.describe_vpn_connections(
	)
        Resources += [R['VpnConnectionId'] for R in response['VpnConnections']]

        ### get vpn gateway
        response = Client.describe_vpn_gateways(
	)
        Resources += [R['VpnGatewayId'] for R in response['VpnGateways']]

    def GetResources(self):
        """Return list of resources for a service"""
        
        try:
            if self.Service == 'ec2':
                return self.GetEc2Resources()
            elif self.Service == 's3':
                response = self.ListBuckets()
                return [Buckets['Name'] for Buckets in response['Buckets']]
            elif self.Service == 'lambda':
                response = self.ListFunctions()
                return [Functions['FunctionName'] for Functions in response['Functions']]
            elif self.Service == 'logs':
                response = self.DescribeLogGroups()
                return [LogGroups['logGroupName'] for LogGroups in response['logGroups']]
            elif self.Service == 'rds':
                response = self.DescribeDbInstances()
                return [Instances['DBInstanceArn'] for Instances in response['DBInstances']]
            elif self.Service == 'es':
                response = self.ListDomainNames()
                DomainNames = [Domains['DomainName'] for Domains in response['DomainNames']]
                response = self.DescribeElasticSearchDomains(DomainNames)
                return [Domains['ARN'] for Domains in response['DomainStatusList']]
            elif self.Service == 'emr':
                response = self.ListClusters()
                return [Clusters['Id'] for Clusters in response['Clusters']]
            elif self.Service == 'dynamodb':
                response = self.ListTables()
                return [Tables for Tables in response['TableNames']]
            elif self.Service == 'firehose':
                response = self.ListDeliveryStreams()
                return [StreamName for StreamName in response['DeliveryStreamNames']]
            elif self.Service == 'glacier':
                response = self.ListVaults()
                return [Vault['VaultName'] for Vault in response['VaultList']]
            elif self.Service == 'kms':
                response = self.ListKeys()
                return [Keys['KeyId'] for Keys in response['Keys']]
            elif self.Service == 'apigateway':
                response = self.GetRestApis()
                return [Item['id'] for Item in response['items']]
            elif self.Service == 'kinesis':
                response = self.ListStreams()
                return [StreamName for StreamName in response['StreamNames']]
            elif self.Service == 'cloudtrail':
                response = self.DescribeTrails()
                return [Trail['TrailARN'] for Trail in response['trailList']]
            elif self.Service == 'sqs':
                response = self.ListQueues()
                return [QueueUrl for QueueUrl in response['QueueUrls']]
            elif self.Service == 'secretsmanager':
                response = self.ListSecrets()
                return [Secret['Name'] for Secret in response['SecretList']]
            elif self.Service == 'cloudfront':
                response = self.ListDistributions()
                response = [V['ARN'] for K,V in response['DistributionList'].items() if 'Items' == K]
            elif self.Service == 'efs':
                response = self.DescribeFileSystems()
                return [FS['FileSystemId'] for FS in response['FileSystems']]
            elif self.Service == 'sagemaker':
                response = self.ListNotebookInstances()
                return [Instance['NotebookInstanceArn'] for Instance in response['NotebookInstances']]
            elif self.Service == 'redshift':
                response = self.DescribeClusters()
                return [Cluster['ClusterIdentifier'] for Cluster in response['Clusters']]
            elif self.Service == 'elasticache':
                response = self.DescribeCacheClusters()
                return [Cluster['CacheClusterId'] for Cluster in response['CacheClusters']]
            elif self.Service == 'workspaces':
                response = self.DescribeWorkspaces()
                return [Workspace['WorkspaceId'] for Workspace in response['Workspaces']]
            elif self.Service == 'ds':
                response = self.DescribeDirectories()
                return [Directory['DirectoryId'] for Directory in response['DirectoryDescriptions']]
            elif self.Service == 'dax':
                response = self.DescribeClusters()
                return [Cluster['ClusterArn'] for Cluster in response['Clusters']]
            elif self.Service == 'route53':
                response = self.ListHostedZones()
                return [HZ['Id'] for HZ in response['HostedZones']]
            elif self.Service == 'directconnect':
                response = self.DescribeVirtualInterfaces()
                return [HZ['virtualInterfaceId'] for HZ in response['virtualInterfaces']]
            elif self.Service == 'datapipeline':
                response = self.ListPipelines()
                return [Pipeline['id'] for Pipeline in response['pipelineIdList']]
            else:
                raise TagNotSupportedError(self.Service)
        except Exception as e:
            raise e

        return []

def UpdateTag(Service, ResourceId, TagName, TagValue):
    """Update tag for services"""


    try:
        Tag = AwsTag(Service, ResourceId)
        Tag.UpdateTag(ResourceId, TagName, TagValue)
    except ClientError as c:
        #raise Exception(type(c))
        raise Exception(c)
    except Exception as e:
        raise e

    return True


def GetServiceName(Service, ResourceId):
    """Return service name""" 

    try:
        Tag = AwsTag(Service, ResourceId)
        return Tag.GetServiceName()
    except ClientError as c:
        #raise Exception(type(c))
        raise Exception(c)
    except Exception as e:
        raise e

    return None


def IsTagExists(Service, ResourceId, TagName):
    """Check if tag name exists"""

    try:
        Tag = AwsTag(Service, ResourceId)
        if Tag.IsTagExists(ResourceId, TagName):
            return True
    except Exception as e:
        ### ignore NoSuchTagSet exception for s3
        if str(e).find('NoSuchTagSet') != -1 and Service == 's3':
            return False
        else:
            raise e

    return False


def GetResources(Service):
    """Get list of resources for service"""

    try:
        Tag = AwsTag(Service)
        return Tag.GetResources()
    except Exception as e:
            raise e

    return []


def GetTagValues(Service, ResourceId, TagNames):
    """Return list of tag values corresponding to tag name for resource"""

    try:
        Tag = AwsTag(Service, ResourceId)
        return Tag.GetTagValues(ResourceId, TagNames)
    except Exception as e:
        ### ignore NoSuchTagSet exception for s3
        if str(e).find('NoSuchTagSet') != -1 and Service == 's3':
            return []
        else:
            raise e

    return []


if __name__ == '__main__':
    Tag = AwsTag('ec2')
    print('I prefer to be a module; however, I can run some tests')
    ServicesExpected = 26
    print('TEST 1: check number of services is', ServicesExpected, 'or more', end='')
    assert Tag.GetServicesCount() >= ServicesExpected
    print('...OK')
