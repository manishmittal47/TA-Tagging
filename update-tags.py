import csv, sys, argparse
from sys import path
path.append('helper')
path.append('C:/Users/cdang/Python/python3.5/packages')
from aws.tag import UpdateTag, IsTagExists, GetServiceName
from ta.log import Log
from ta.services import GetB3ServiceName

#################################################
#                                               #
#            DEFINE VARIABLES                   #
#                                               #
#################################################

LogFileName = 'tagging.log'
Overwrite = False

#################################################
#                                               #
#            DEFINE FUNCTIONS                   #
#                                               #
#################################################



#################################################
#                                               #
#            PROGRAM ENTRY                      #
#                                               #
#################################################

if __name__ == '__main__':

    ### exit if not python 3
    try:
        PyVerMin = (3,0)
        assert sys.version_info >= PyVerMin
    except Exception as e:
        print('You are using Python ' + sys.version[0] + ', but this program requires Python', PyVerMin[0])
        sys.exit()


    ### check command line arguments: --tag AwsTagName=CsvTagName
    parser = argparse.ArgumentParser()
    parser.add_argument('--overwrite', nargs=1, required=False, metavar='yes|no', choices=['yes', 'no'], \
                        default=argparse.SUPPRESS, help='yes to overwrite existing tag, and no will not \
                        overwrite')
    parser.add_argument('--tag', nargs=1, required=True, metavar='AwsTag=CsvTag', help='tag \
                        formatted as AwsTag=CsvTag, where AwsTag is the tag name in AWS, and CsvTag \
                        is the tag name in the csv file')
    parser.add_argument('--csvfile', nargs=1, metavar='filename', type=argparse.FileType('r', encoding='UTF-8'), \
                        required=True, help='data file in csv format')
    # arg = ('param', ['value']) -> ('tag', ['Channel=hello'])
    for arg in vars(parser.parse_args()).items():
        if arg[0] == 'overwrite':
            Overwrite = True if arg[1][0] == 'yes' else False
        elif arg[0] == 'tag':
            if arg[1][0].find('=') != -1: #Channel=tag_channel
                AwsTagName, CsvTagName = arg[1][0].split('=')
            else:
                print('--tag value is invalid. See --help.')
                sys.exit()
        elif arg[0] == 'csvfile':
            reader = arg[1][0] #read file stream

    ### initialize local variable
    TagPropIndex = {CsvTagName: None, 'resource_id': None, 'service': None}

    ### initialize logging: Level can be INFO or DEBUG
    L = Log(Filename='tagging.log', Level='INFO')

    ### print starting divider
    L.TeeLog('----------------------------------------------------------')

    ### open csv file
    try:
        CsvReader = csv.reader(reader)
    except Exception as e:
        L.TeeLog("Failed to open file:", e)
        sys.exit()

    ### get tag properties index in first row
    try:
        for row in CsvReader:
            for K in TagPropIndex.keys():
                TagPropIndex[K] = row.index(K)
            break
    except Exception as e:
        L.TeeLog('Failed to get index:', e)
        sys.exit()

    ### counters
    RowCounter = 0
    UpdateSucceedCounter = 0
    UpdateFailedCounter = 0
    UpdateSkipCounter = 0

    ### continue to process csv file
    try:
        TagIdx = TagPropIndex[CsvTagName]
        ResourceIdx = TagPropIndex['resource_id']
        ServiceIdx = TagPropIndex['service']

        ### each row in csv
        for row in CsvReader:
            TagName = AwsTagName
            TagValue = row[TagIdx]
            ResourceId = row[ResourceIdx]
            Service = GetB3ServiceName(row[ServiceIdx])

            RowCounter += 1

            L.TeeLog('Tag #' + str(RowCounter) + ': ResourceId=' + str(ResourceId) + ' TagName='\
	                + str(TagName) + ' TagValue=' + str(TagValue) + ' Service=' \
			+ GetServiceName(Service, ResourceId))

            ### skip if tag value is Unknown or None
            if TagValue.lower() == 'unknown' or TagValue.lower() == 'none':
                L.TeeLog('Skip update since tag equals None or Unknown')
                UpdateSkipCounter += 1
                continue

            ### skip if Overwrite is False and tag already exists
            try:
                if not Overwrite and IsTagExists(Service, ResourceId, TagName):
                    L.TeeLog('Skip update for ' + ResourceId + ' since tag ' + TagName + ' exists and Overwrite is ' \
                             + str(Overwrite))
                    UpdateSkipCounter += 1
                    continue
            except Exception as e:
                L.TeeLog('Skip update since we cannot verify whether tag name ' + TagName + ' exists: ' + str(e), 1)
                UpdateSkipCounter += 1
                continue

            ### update tag
            try:
                if UpdateTag(Service, ResourceId, TagName, TagValue):
                    L.TeeLog('Successfully updated resourceid=' + ResourceId)
                    UpdateSucceedCounter += 1
                else:
                    L.TeeLog('Failed to update resourceid=' + ResourceId)
                    UpdateFailedCounter += 1
            except Exception as e:
                if str(e).find('OperationAborted') != -1 and Service == 's3':
                    L.TeeLog('Encountered a known exception while trying to update s3 bucket tag that can typically be ignored and assumed successful on resourceid=' + ResourceId + ': ' + str(e))
                    UpdateSucceedCounter += 1
                else:
                    L.TeeLog('Failed to update resourceid=' + ResourceId + ': ' + str(e))
                    UpdateFailedCounter += 1
    except Exception as e:
        L.TeeLog('Error processing csv file:', e)
    finally:
        reader.close()

    ### print summary
    L.TeeLog('Summary: Total=' + str(RowCounter) + ' Successful=' + str(UpdateSucceedCounter) + ' Skip=' + \
            str(UpdateSkipCounter) + ' Failed=' + str(UpdateFailedCounter) + ' Overwrite=' + str(Overwrite))

else:
    L.TeeLog('I\'m not a module.')
    sys.exit()
