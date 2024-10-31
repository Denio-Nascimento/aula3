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

## Passo 1

Configurar um Site estático básico

- S3
- CloudFront

## Passo 2

Configurar um Site estático para consultar o pedido do DynamoDB

- S3
- CloudFront
- API GATEWAY
- LAMBDA
- DYNAMODB
