from flask import Flask, request
import boto3
import json
import os

# aws_access_key_id and aws_secret_access_key are used to define the user we will be using for the api
# to integrate with sqs
aws_access_key_id = os.environ['Producer_user_access_key_id']
aws_secret_access_key = os.environ['Producer_user_secret_access_key']
app = Flask(__name__)

# AWS_REGION is used in order to define in which aws region we are working
AWS_REGION = 'us-east-1'
# queue_url defines the endpoint of the sqs service for us to send our messages to
queue_url = os.environ['QueueUrl']
# sqs_client is using the boto3 library to enable us to run commands on the sqs service
sqs_client = boto3.client("sqs", region_name=AWS_REGION, aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)


# @app.route is using the flask library to define which uri should we use and for what methods
# inside the api we have a function the takes the json file from the post request and sends it to sqs
# we use try and except for exception handling

@app.route('/api', methods=['POST'])
def post():
    request_data = request.get_json()
    body = json.dumps(request_data)
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=body

        )
        return (response)
    except sqs_client.exceptions.ClientError:
        print('The IAM user does not have permission to send messages to the queue')
    except sqs_client.errorfactory.QueueDoesNotExist:
        print('The Queue Url is not correct or the queue does not exist')

# app.run is responsible for the api to run when the code executes, it contains the host listening ip and ports

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")