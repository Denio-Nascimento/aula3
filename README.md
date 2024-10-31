# Criação do conteúdo para o arquivo README.md

# Conteúdo detalhado do README.md
readme_content = """
# AWS Dynamic Site with API Gateway, Lambda, and DynamoDB

This project demonstrates a complete AWS architecture that integrates a static site hosted on S3 with an API Gateway, Lambda, and DynamoDB. The static site allows users to query order information from a DynamoDB table using a serverless architecture for a fast, scalable, and secure experience.

## Project Architecture

1. **Amazon S3** - Hosts the static site files (HTML, CSS, JavaScript).
2. **Amazon CloudFront** - Distributes the S3 site globally and provides a secure entry point.
3. **Amazon API Gateway** - Acts as the entry point for API calls from the site to AWS Lambda.
4. **AWS Lambda** - Processes API requests, retrieves data from DynamoDB, and sends responses.
5. **Amazon DynamoDB** - Stores order information for quick retrieval.

## Prerequisites

- AWS account
- Basic knowledge of AWS services (S3, API Gateway, Lambda, and DynamoDB)
- Files for the static site (HTML, CSS, JavaScript)

---

## Step-by-Step Setup

### 1. Set Up DynamoDB

1. In the AWS Console, go to **DynamoDB** and create a table named `Orders`.
2. Define the table with a primary key `orderId` (String) and add any additional fields like `customerName`, `orderDate`, `status`, etc.
3. Insert some sample records to be used for testing.

### 2. Configure AWS Lambda

1. Go to **AWS Lambda** and create a new Lambda function named `GetOrderDetails`.
2. Add the following Python code to your Lambda function:

   ```python
   import json
   import boto3
   from botocore.exceptions import ClientError

   dynamodb = boto3.resource('dynamodb')
   table = dynamodb.Table('Orders')

   def lambda_handler(event, context):
       order_id = event.get('queryStringParameters', {}).get('orderId')
       if not order_id:
           return {'statusCode': 400, 'body': json.dumps({'message': 'Order ID is required'})}

       try:
           response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('orderId').eq(order_id))
           items = response.get('Items', [])
           if not items:
               return {'statusCode': 404, 'body': json.dumps({'message': 'Order not found'})}

           return {
               'statusCode': 200,
               'headers': {
                   'Access-Control-Allow-Origin': '*',
                   'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                   'Access-Control-Allow-Methods': 'OPTIONS,GET'
               },
               'body': json.dumps(items)
           }
       except ClientError as e:
           return {
               'statusCode': 500,
               'headers': {
                   'Access-Control-Allow-Origin': '*',
                   'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                   'Access-Control-Allow-Methods': 'OPTIONS,GET'
               },
               'body': json.dumps({'message': 'Error accessing DynamoDB', 'error': str(e)})
           }
