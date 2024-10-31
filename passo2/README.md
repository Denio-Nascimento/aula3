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
```

3. Atribua as permissões necessárias para que a Lambda acesse o DynamoDB.
4. Teste a função com um `orderId` de exemplo para garantir que ela recupera os dados corretamente.

### 3. Configurar o API Gateway

1. Acesse **API Gateway** e crie uma nova **API REST**.
2. Defina um novo recurso `/orders` e adicione o método **GET** a esse recurso.
3. Integre o método GET com sua função Lambda usando **Lambda Proxy Integration**.
4. Habilite **CORS**:
   - Vá em **Actions > Enable CORS** e configure `Access-Control-Allow-Origin`, `Access-Control-Allow-Headers` e `Access-Control-Allow-Methods`.
5. Implemente a API criando um novo stage (por exemplo, `prod`).

### 4. Configurar o S3 e o CloudFront para o Site Estático

#### Bucket S3

1. Crie um **bucket S3** e faça o upload dos arquivos do site (HTML, CSS, JS).
2. Configure o bucket para **hospedagem de site estático**, mantendo-o **privado** (sem acesso público).

#### CloudFront

1. Crie uma **distribuição CloudFront** com o bucket S3 como origem.
2. Crie uma **Identidade de Acesso de Origem (OAI)** e associe-a ao CloudFront para restringir o acesso ao S3.
3. Atualize a política do bucket S3 para permitir acesso apenas através do CloudFront.

### 5. Conectar o Site Estático à API

1. No arquivo JavaScript (`site.js`), configure uma chamada AJAX para o endpoint do API Gateway.
2. Exemplo (site.js):

```javascript
$(document).ready(function () {
    $('#consultOrder').click(function () {
        var orderId = $('#order_id').val();
        if (orderId) {
            $.ajax({
                url: `https://your-api-id.execute-api.region.amazonaws.com/prod/orders?orderId=${orderId}`,
                method: 'GET',
                success: function (data) {
                    // Tratamento dos dados recebidos
                },
                error: function (error) {
                    alert('Erro ao consultar pedido!');
                }
            });
        } else {
            alert('Por favor, insira o código do pedido.');
        }
    });
});
```
## Explicação dos Conceitos Principais

### Configuração de CORS

CORS é essencial quando o frontend e o backend estão em domínios diferentes. Os cabeçalhos configurados na Lambda e no API Gateway (`Access-Control-Allow-Origin`, `Access-Control-Allow-Headers`, e `Access-Control-Allow-Methods`) garantem que o navegador permita requisições entre diferentes origens. Essa configuração é fundamental para evitar bloqueios de segurança do navegador e permitir que o site estático comunique-se com a API.

### Integração Proxy do API Gateway com Lambda

A Integração Proxy permite que o API Gateway passe detalhes da solicitação diretamente para a Lambda, como parâmetros de consulta, cabeçalhos e corpo da requisição. Isso simplifica o código Lambda, pois a função recebe todos os detalhes da solicitação em um formato JSON padrão, facilitando o tratamento de dados e respostas.

### CloudFront com Acesso Privado ao S3

Usando o CloudFront com uma Identidade de Acesso de Origem (OAI), mantemos o bucket S3 privado, permitindo acesso somente através do CloudFront. Essa configuração melhora a segurança do conteúdo estático, garantindo que apenas o CloudFront possa acessar o bucket. Além disso, o CloudFront proporciona uma distribuição global do conteúdo, melhorando a velocidade de carregamento para usuários em diferentes locais geográficos.

---

## Testando o Projeto

1. Abra a URL do CloudFront no navegador.
2. Insira um `orderId` no campo de entrada e clique em "Consultar Pedido".
3. Os detalhes do pedido devem ser recuperados e exibidos na página.

---

## Melhorias Futuras

- **Autenticação**: Integre o AWS Cognito para autenticação de usuários e proteção de dados sensíveis.
- **Tratamento de Erros**: Melhore o tratamento de erros no frontend para exibir mensagens mais informativas para os usuários.
- **Integração com SDK**: Em futuros projetos, considere usar o SDK do API Gateway para simplificar a integração e a manutenção do código.

---

## Licença

Este projeto é open-source e está disponível sob a [Licença MIT](LICENSE).


