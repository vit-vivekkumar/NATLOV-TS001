import boto3
from botocore.exceptions import NoCredentialsError

# Initialize a session using LocalStack git auth test
sqs = boto3.client(
    'sqs',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    aws_session_token='test',
    region_name='us-east-1',
    endpoint_url='http://localhost:4566'
)

# Send a message to the queue
response = sqs.send_message(
    QueueUrl='http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/test-queue',
    MessageBody='Hello, this is a test message from Django!'
)
print(f"Message ID: {response['MessageId']}")

# Receive a message from the queue
response = sqs.receive_message(
    QueueUrl='http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/test-queue'
)
if 'Messages' in response:
    for message in response['Messages']:
        print(f"Message Body: {message['Body']}")
        print(f"Message : {message}")
        receipt_handle = message['ReceiptHandle']

        # Delete received message from the queue
        sqs.delete_message(
            QueueUrl='http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/test-queue',
            ReceiptHandle=receipt_handle
        )
        print(f"Deleted message with ID: {message['MessageId']}")
