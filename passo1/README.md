
# AWS na Veia - Hospedagem de Site Estático com S3 e CloudFront

Este repositório contém os arquivos para um site estático que será hospedado na AWS utilizando S3 e CloudFront. O objetivo é garantir uma hospedagem segura, tornando o bucket S3 privado e usando o CloudFront para controlar o acesso.

## Índice
- [Arquitetura](#arquitetura)
- [Recursos da AWS Utilizados](#recursos-da-aws-utilizados)
  - [Amazon S3](#amazon-s3)
  - [Amazon CloudFront](#amazon-cloudfront)
  - [Política de IAM](#política-de-iam)
- [Instruções de Configuração](#instruções-de-configuração)
  - [Passo 1: Criar um Bucket S3](#passo-1-criar-um-bucket-s3)
  - [Passo 2: Configurar a Política do Bucket](#passo-2-configurar-a-política-do-bucket)
  - [Passo 3: Fazer Upload dos Arquivos para o S3](#passo-3-fazer-upload-dos-arquivos-para-o-s3)
  - [Passo 4: Criar uma Distribuição CloudFront](#passo-4-criar-uma-distribuição-cloudfront)
  - [Passo 5: Testar a Configuração](#passo-5-testar-a-configuração)

## Arquitetura

Este setup utiliza:
1. **Amazon S3** para armazenar os arquivos estáticos (HTML, CSS, imagens).
2. **Amazon CloudFront** como uma Content Delivery Network (CDN) para entregar os arquivos de forma segura a partir do bucket S3 privado.

### Recursos da AWS Utilizados

#### Amazon S3
- **Propósito**: O S3 armazenará os arquivos HTML, CSS e imagem que compõem este site estático. O bucket será configurado como privado, permitindo acesso apenas através do CloudFront.
- **Configurações**: Habilitar criptografia no lado do servidor (recomendado para produção), versionamento e definir permissões como privadas.

#### Amazon CloudFront
- **Propósito**: O CloudFront atuará como a CDN, armazenando em cache e entregando os ativos do site globalmente. Ele garante que apenas o CloudFront possa acessar o bucket S3.
- **Configurações**: Configurar um controle de acesso de origem (OAC) para limitar o acesso ao bucket S3 ao CloudFront.

#### Política de IAM
- **Propósito**: Uma política de IAM controlará as permissões para gerenciar o S3, CloudFront e outros recursos AWS necessários.

## Instruções de Configuração

Siga estes passos para configurar a hospedagem do site estático com S3 e CloudFront.

### Passo 1: Criar um Bucket S3

1. Abra o [console do Amazon S3](https://s3.console.aws.amazon.com/s3/).
2. Escolha **Criar bucket**.
3. Forneça um **Nome exclusivo para o bucket** (ex: `aws-na-veia-static-site`).
4. Selecione a **Região da AWS**.
5. Clique em **Criar bucket**.

### Passo 2: Configurar a Política do Bucket

Esta política de bucket permitirá que o CloudFront acesse o bucket enquanto o mantém privado para o público.

1. Vá para a aba **Permissões** do seu bucket S3.
2. Em **Política de bucket**, adicione o seguinte JSON, substituindo `SEU-ID-DISTRIBUICAO-CLOUDFRONT` pelo ID da sua distribuição CloudFront e `NOME-DO-SEU-BUCKET` pelo nome do bucket S3.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::NOME-DO-SEU-BUCKET/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::SEU-ID-DISTRIBUICAO-CLOUDFRONT"
                }
            }
        }
    ]
}
```

### Passo 3: Fazer Upload dos Arquivos para o S3

1. Na aba **Objetos** do bucket S3, escolha **Upload**.
2. Faça upload dos arquivos `index.html`, `styles.css`, e `aws_na_veia_logo.webp`.
3. Defina as permissões dos arquivos como privadas.

### Passo 4: Criar uma Distribuição CloudFront

1. Abra o [console do Amazon CloudFront](https://console.aws.amazon.com/cloudfront/).
2. Escolha **Criar Distribuição**.
3. Em **Configurações de Origem**:
   - Defina **Origem** com o nome do seu bucket S3.
   - Habilite **Restringir Acesso ao Bucket** e crie um novo **Controle de Acesso de Origem (OAC)** para garantir que apenas o CloudFront possa acessar o bucket S3.
4. **Comportamento de Cache**:
   - Defina **Política de Protocolo do Visualizador** para **Redirecionar HTTP para HTTPS**.
   - Personalize as configurações de cache conforme necessário.
5. **Configurações de Distribuição**:
   - Configure outras configurações como SSL se necessário.
6. Clique em **Criar Distribuição**.

### Passo 5: Testar a Configuração

1. Aguarde a distribuição do CloudFront ser implementada.
2. Acesse a URL do CloudFront para garantir que o site seja carregado corretamente.
3. Verifique se acessar diretamente o bucket S3 retorna uma mensagem de acesso negado, garantindo que o bucket esteja privado.

---

Este setup garante uma solução segura e escalável para hospedar seu site estático utilizando AWS.

Certifique-se de substituir valores de placeholders (como `NOME-DO-SEU-BUCKET` e `SEU-ID-DISTRIBUICAO-CLOUDFRONT`) pelos valores reais da sua configuração AWS.
