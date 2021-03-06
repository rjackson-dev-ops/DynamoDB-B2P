# Find students within a country
# A Cloud Guru - Dynamo DB Course\
# USES V3 DATA MODEL

import boto3, botocore, tqdm, random, time
from time import gmtime, strftime
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from sys import version_info
py3 = version_info[0] > 2 #creates boolean value for test that Python major version > 2

lesson = '4-014' ## UDPATE ME
loadmin_session = boto3.Session()
db_c = loadmin_session.client('dynamodb')
db_r = loadmin_session.resource('dynamodb')

## PREREQS - images/ folder in same directory as this scripts
##          configured AWS tools
##          installed python2.7+
##          installed boto3 (pip install boto3)
##          Installed faker module
##          Installed tqdm module
##          'loadmin' AWS configuration profile - with admin rights
##          Data Model v2 loaded.
##          _retry.json file from lesson files - adjusted for 1mil+ auto retries
##              for retryable operations

if __name__ == "__main__":
    student_id = ""
    capacityconsumed = 0
    scannedcount = 0


    while True:
        if py3:
            student_id = str(input('Enter a student ID: '))
        else:
            student_id = str(raw_input('Enter a student ID: '))
        if student_id !="":
            break
    ## END WHILE LOOP
    starttime = time.time()
    response=db_r.Table("lo_courseregistration").scan(\
        ReturnConsumedCapacity='TOTAL', \
        ExpressionAttributeValues={':student_id' : student_id}, \
        FilterExpression="s_id = :student_id" \
    )
    capacityconsumed = response['ConsumedCapacity']['CapacityUnits']
    scannedcount = response['ScannedCount']

    data=response['Items']
    while 'LastEvaluatedKey' in response:
        #print "hi"
        response=db_r.Table("lo_courseregistration").scan(\
            ReturnConsumedCapacity='TOTAL', \
            ExpressionAttributeValues={':student_id' : student_id}, \
            ExclusiveStartKey=response['LastEvaluatedKey'], \
        FilterExpression="s_id = :student_id" \
        )
        #print response
        capacityconsumed = capacityconsumed + response['ConsumedCapacity']['CapacityUnits']
        scannedcount = scannedcount + response['ScannedCount']
        data.extend(response['Items'])

    finishtime=time.time()
    timetocomplete = finishtime - starttime
    print "Script Started on %s, finished on %s, took %0.2fs to complete without indexes" % (time.ctime(starttime),\
                time.ctime(finishtime), timetocomplete)
    print "Operation required %i capacity units to complete" % capacityconsumed
    print "Total number of items scanned [%i]" % scannedcount
    print "Located [%i] courses for student [%s]" % (len(data), student_id)
    print "Press Q to quit... or any other key to list courses for student %s" % student_id

    if py3:
        entry = str(input()).lower()
    else:
        entry = str(raw_input()).lower()
    if entry == 'q':
        exit(0)
    print "#\tS_ID\tCourse Instance"
    for i, s_instance in enumerate(data):
        print "%d\t%s\t%s" % (i+1, \
        s_instance['s_id'], s_instance['ci_id'])
