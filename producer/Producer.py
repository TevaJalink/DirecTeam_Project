from flask import Flask, request
import boto3
import botocore
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
sqs_client = boto3.client("sqs", region_name=AWS_REGION,aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)


# @app.route is using the flask library to define which uri should we use and for what methods
@app.route('/api', methods=['POST'])
def post():
    # request_data is using the request library in flask to receive the json file from the post command
    request_data = request.get_json()
    # body is turning the json to a string
    body = json.dumps(request_data)
    # response is used to define the boto3 command to send a message to the sqs endpoint (QueueUrl is the endpoint url)
    # and MessageBody is the content of the message
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=body

        )
        # return is used to send back information to the client
        return (response)
    except botocore.exceptions.ClientError:
        print('The IAM user does not have permission to send messages to the queue')
    except botocore.errorfactory.QueueDoesNotExist:
        print('The Queue Url is not correct or the queue does not exist')


# the if is running only when the API script is being used from the original path so debug mode would not run
# when containarized
if __name__ == "__main__":
    app.run(debug=True)