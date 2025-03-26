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
