import json
import boto3
import PyPDF2
from io import BytesIO
import base64

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Flashcards')

def lambda_handler(event, context):
    print("Event:", json.dumps(event))
    try:
        http_method = event['requestContext']['http']['method']
        print("HTTP Method:", http_method)
        if http_method == 'POST':
            return handle_upload(event)
        elif http_method == 'GET':
            return handle_get_flashcards(event)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Unsupported method')
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Internal server error: {str(e)}")
        }

def handle_upload(event):
    try:
        body = json.loads(event['body'])
        pdf_data = body['pdf_data']
        document_id = body['document_id']

        # Decode base64-encoded PDF data
        pdf_content = base64.b64decode(pdf_data)

        # Upload PDF data to S3
        s3.put_object(Bucket='uploaded-fc-pdfs', Key=f'{document_id}.pdf', Body=pdf_content)

        return {
            'statusCode': 200,
            'body': json.dumps('PDF uploaded successfully')
        }
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Upload error: {str(e)}")
        }

def handle_get_flashcards(event):
    try:
        document_id = event['queryStringParameters']['document_id']

        response = table.get_item(Key={'docID': document_id})
        flashcards = response.get('Item', {}).get('flashcards', [])

        return {
            'statusCode': 200,
            'body': json.dumps(flashcards)
        }
    except Exception as e:
        print(f"Get flashcards error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Get flashcards error: {str(e)}")
        }
