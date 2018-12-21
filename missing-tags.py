import csv, sys, argparse
from sys import path
path.append('helper')
path.append('C:/Users/cdang/Python/python3.5/packages')
from aws.tag import UpdateTag, IsTagExists, GetResources, GetTagValues
from ta.log import Log
from ta.services import GetB3ServiceName, GetServices
from ta.tools import GetKeys
import boto3


### open csv file
try:
    WriteStream = open('missing-tags.csv', 'w', newline='')
    CsvWriter = csv.writer(WriteStream, delimiter=',')
except Exception as e:
    print("Failed to open file:", e)
    sys.exit()

### write header to csv
CsvWriter.writerow(['resource_id'] + ['service'] + ['tag_channel'] + ['tag_billing_cost_center'] + ['tag_name'] + \
                   ['tag_environment'])


### TEST - use variable to control services to test - remove in prod
ServicesToTest = ['s3']


### get services dictionary of CsvServiceName to B3ServiceName, i.e. AmazonApiGateway: apigateway
Services = GetServices()
ResourcesDiscovered = {}
for CsvService, B3Service in Services.items():

    ### TEST - REMOVE IN PROD
    if B3Service not in ServicesToTest:
        continue

    try:
        print(CsvService, ':', B3Service, '::: Gathering resources')
        #Resources = GetResources(B3Service) if B3Service == 'lambda' else [] ###DEBUG - REMOVE WHEN DONE
        Resources = GetResources(B3Service)
        ResourcesDiscovered[CsvService] = len(Resources)
    except Exception as e:
        print(CsvService, ':', B3Service, '::: Skip ... unable to get resources:', e)
        continue
    if len(Resources) == 0:
        print(CsvService, ':', B3Service, '::: There are no resources')
    else:
        TagName = 'Channel'
        print(CsvService, ':', B3Service, '::: There are', len(Resources), 'resources')
        for ResourceId in Resources: 
            print(CsvService, ':', B3Service,'::: Check whether resource id', ResourceId, 'has tag', TagName)
            try:
                if not IsTagExists(B3Service, ResourceId, TagName):
                    print(CsvService, ':', B3Service, '::: Adding resource id', ResourceId, 'to csv file since tag', TagName, 'missing')

                    ### look up other tags
                    Tags = {'Channel': '', 'BillingCostCenter': '', 'Name': '', 'Environment': ''}
                    TempTags = GetTagValues(B3Service, ResourceId, list(Tags)) #[{TagName: TagValue}, {}, {}]
                    for Tag in TempTags:
                        for T,V in Tag.items():
                            if T in Tags:
                                Tags[T] = V

                    print(CsvService, ':', B3Service, '::: Other tags for resource id', ResourceId, 'includes', Tags)
                    # write to csv
                    CsvWriter.writerow([ResourceId] + [CsvService] + [Tags['Channel']] + [Tags['BillingCostCenter']] + \
		                       [Tags['Name']]  + [Tags['Environment']])
                else:
                    print(CsvService, ':', B3Service, '::: Tag', TagName, 'exists for resource', ResourceId, 'so will not add to csv file')
            except Exception as e:
                print(CsvService, ':', B3Service, '::: Skip ... unable to verify tag exists:', e)

### print summary
print('Resources Discovered:', ResourcesDiscovered)

### close stream
WriteStream.close()
