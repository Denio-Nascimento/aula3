import json
import boto3
from botocore.exceptions import ClientError

# Inicializando o cliente DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PedidosTable')  # Substitua 'Orders' pelo nome da sua tabela

def lambda_handler(event, context):
    # Log do evento recebido para depuração
    print("Evento recebido:", event)
    
    # Extraindo o ID do pedido dos parâmetros de consulta
    order_id = event.get('queryStringParameters', {}).get('orderId')
    
    # Verificando se o ID do pedido foi fornecido
    if not order_id:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps({'message': 'Parâmetro "orderId" é obrigatório.'})
        }
    
    try:
        # Consultando o DynamoDB usando o orderId
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('orderId').eq(order_id)
        )
        
        # Obter os itens do pedido
        items = response.get('Items', [])
        
        # Verificar se o pedido foi encontrado
        if not items:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'OPTIONS,GET'
                },
                'body': json.dumps({'message': 'Pedido não encontrado.'})
            }
        
        # Retornar os detalhes do pedido
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps(items)  # Retorna os itens encontrados
        }
        
    except ClientError as e:
        # Log do erro para depuração
        print("Erro ao acessar o DynamoDB:", e)
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,GET'
            },
            'body': json.dumps({'message': 'Erro ao acessar o DynamoDB', 'error': str(e)})
        }
