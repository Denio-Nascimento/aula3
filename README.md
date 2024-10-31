# Site Dinâmico na AWS com API Gateway, Lambda e DynamoDB

Este projeto demonstra uma arquitetura completa na AWS que integra um site estático hospedado no S3 com um API Gateway, Lambda e DynamoDB. O site permite que usuários consultem informações de pedidos em um banco de dados DynamoDB utilizando uma arquitetura serverless, proporcionando uma experiência rápida, escalável e segura.

## Arquitetura do Projeto

1. **Amazon S3** - Hospeda os arquivos do site estático (HTML, CSS, JavaScript).
2. **Amazon CloudFront** - Distribui o site globalmente, garantindo rapidez e segurança.
3. **Amazon API Gateway** - Atua como ponto de entrada para chamadas da API do site para o AWS Lambda.
4. **AWS Lambda** - Processa as solicitações da API, recupera dados do DynamoDB e retorna respostas.
5. **Amazon DynamoDB** - Armazena informações de pedidos para consulta rápida.

## Pré-requisitos

- Conta AWS
- Conhecimento básico dos serviços AWS (S3, API Gateway, Lambda e DynamoDB)
- Arquivos do site estático (HTML, CSS, JavaScript)

---

## Passo a Passo para Configuração

### 1. Configurar o DynamoDB

1. No console da AWS, vá para **DynamoDB** e crie uma tabela chamada `Orders`.
2. Defina a tabela com a chave primária `orderId` (String) e adicione outros campos como `customerName`, `orderDate`, `status`, etc.
3. Insira alguns registros de exemplo para testes.

### 2. Configurar o AWS Lambda

1. Acesse o **AWS Lambda** e crie uma nova função chamada `GetOrderDetails`.
2. Adicione o seguinte código Python à sua função Lambda:

   ```python
   import json
   import boto3
   from botocore.exceptions import ClientError

   dynamodb = boto3.resource('dynamodb')
   table = dynamodb.Table('Orders')

   def lambda_handler(event, context):
       order_id = event.get('queryStringParameters', {}).get('orderId')
       if not order_id:
           return {'statusCode': 400, 'body': json.dumps({'message': 'Order ID é obrigatório'})}

       try:
           response = table.query(KeyConditionExpression=boto3.dynamodb.conditions.Key('orderId').eq(order_id))
           items = response.get('Items', [])
           if not items:
               return {'statusCode': 404, 'body': json.dumps({'message': 'Pedido não encontrado'})}

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
               'body': json.dumps({'message': 'Erro ao acessar o DynamoDB', 'error': str(e)})
           }
