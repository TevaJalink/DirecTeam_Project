# this script is used to poll messages from sqs and push them as files to s3 bucket
import boto3
import json
import flatdict
import os
from datetime import datetime

# aws_access_key_id and aws_secret_access_key are used to define the user we will be using for the consumer to receive
# messages from the sqs and put them in the s3 bucket
aws_access_key_id = os.environ['Consumer_user_access_key_id']
aws_secret_access_key = os.environ['Consumer_user_secret_access_key']
# AWS_REGION is used to define which region we are working in
AWS_REGION = 'us-east-1'
# queue_url is used to define the endpoint of the sqs service
queue_url = os.environ['QueueUrl']
# sqs_client is used with the boto3 library in order to talk with sqs
sqs_client = boto3.client("sqs", region_name=AWS_REGION, aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
# while is being used to create an infinite loop
# inside the loop we try to take messages from the sqs queue and check for the key word Messages, if the word
# exists then the function will take it, extract the json and push it as a csv to s3 bucket

while True:
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url
        )
    except sqs_client.exceptions.ClientError:
        print('The IAM user does not have the required permissions to poll messages')
        break
    except sqs_client.errorfactory.QueueDoesNotExist:
        print('The Queue Url is not correct or the queue does not exist')
        break
    if 'Messages' in response:
        Body = response['Messages'][0]['Body']
        json_format = json.loads(Body)
        flattened_dict = flatdict.FlatDict(json_format, delimiter='.')
        File_content = str(flattened_dict)
        date_time = datetime.now()
        date_time_str = str(date_time)
        # Consumer_S3_Bucket_Name will define tha name of the s3 bucket
        Consumer_S3_Bucket_Name = os.environ['S3_Bucket_Name']
        Consumer_S3_Bucket_Name_String = str(Consumer_S3_Bucket_Name)
        # line 53-57 are responsible for updating the csv to s3 bucket using boto3 library
        try:
            s3 = boto3.resource('s3', region_name=AWS_REGION, aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
            Create_File = s3.Object(Consumer_S3_Bucket_Name_String, 'post_processing/consumer_output ' + date_time_str
                                    + '.csv')
            result = Create_File.put(Body=str(File_content))
        except s3.exceptions.ClientError:
            print('The IAM user does not have permissions to create objects in s3,'
                  ' The bucket name is incorrect or bucket does not exist')
            break
        # now we will erase the message from sqs, http_status is the status code we get back from s3, if we don't get
        # 200 we would want to let the message back to the queue to be processed again, we delete the messages based
        # on the unique ID ReceiptHandle
        http_status = result['ResponseMetadata']['HTTPStatusCode']
        if http_status == 200:
            try:
                message_handle = response['Messages'][0]['ReceiptHandle']
                remove_messages = sqs_client.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message_handle
                )
            except sqs_client.exceptions.ClientError:
                print('The IAM user does not have permission to remove messages from the queue')
                break
            except sqs_client.errorfactory.QueueDoesNotExist:
                print('The Queue Url is not correct or the queue does not exist')
                break