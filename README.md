# M26
Gen AI

a chatbot that connects with a bucket and manages policy documents using Python, you will need to follow these steps:

Set up the chatbot framework.
Integrate with a cloud storage service (e.g., AWS S3).
Implement functionality to retrieve and manage policy documents.
Here’s a step-by-step guide along with the Python code:

Step 1: Set up the Chatbot Framework
You can use a simple framework like Flask to set up the chatbot backend.

Python
# Install dependencies
# pip install flask boto3

from flask import Flask, request, jsonify
import boto3
import os

app = Flask(__name__)

# Configure AWS SDK
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

bucket_name = 'YOUR_BUCKET_NAME'

@app.route('/list-documents', methods=['GET'])
def list_documents():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        documents = [item['Key'] for item in response.get('Contents', [])]
        return jsonify(documents)
    except Exception as e:
        return str(e), 500

@app.route('/get-document', methods=['GET'])
def get_document():
    document_key = request.args.get('key')
    if not document_key:
        return "Document key is required", 400
    try:
        response = s3.get_object(Bucket=bucket_name, Key=document_key)
        document_content = response['Body'].read().decode('utf-8')
        return jsonify({'content': document_content})
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
 2 vulnerabilities detected
Explanation:
Install Dependencies:

flask for the web framework.
boto3 for AWS SDK to interact with S3.
Configure AWS SDK:

Set up the AWS SDK with your access keys and region.
Ensure the environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set.
List Documents Endpoint:

/list-documents: Lists all documents in the specified S3 bucket.
Uses s3.list_objects_v2 to fetch the list of objects in the bucket.
Returns a JSON response with the list of document keys.
Get Document Endpoint:

/get-document: Retrieves the content of a specified document from the S3 bucket.
Requires a key query parameter to specify the document.
Uses s3.get_object to fetch the document content.
Returns a JSON response with the document content.
Running the Bot
Set Environment Variables:

Ensure your AWS credentials and region are set as environment variables:
sh
export AWS_ACCESS_KEY_ID='your_access_key_id'
export AWS_SECRET_ACCESS_KEY='your_secret_access_key'
export AWS_REGION='your_region'
export BUCKET_NAME='your_bucket_name'
Run the Flask Application:

sh
python app.py
Test the Endpoints:

Use a tool like curl or Postman to test the endpoints:
sh
curl http://127.0.0.1:5000/list-documents
curl http://127.0.0.1:5000/get-document?key=your_document_key
This example sets up a basic chatbot with endpoints to list and retrieve policy documents from an S3 bucket. You can extend this functionality by adding more endpoints and handling additional actions as needed.
