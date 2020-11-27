# API para o serviço de Confiabilidade

Essa API fornece o serviço de processamento de repositório, retornando um link para a imagem resultante desse processamento.
Quando a solitação é feita, é retornado um `token de status` que irá está associado a um processamento. Com esse token é possível obter o status do processamento.
Quando o processamento é finalizado, a rota de status do processamento irá returnar o link para a imagem resultante.


<br><br>
## Rodar locamente

#### 1. Crie uma conta no [imgur](https://imgur.com/)
#### 2. Registre uma aplicação na sua conta do imgur ([link](https://api.imgur.com/oauth2/addclient)).

> Durante o registro seleciona a opção `OAuth 2 authorization without a callback URL`

#### 3. Atualize o arquivo `.env` com seu `CLIENT_ID`

#### 4. Rode o comando abaixo para não deixar o git rastrear o arquivo `.env`

```
git update-index --assume-unchanged .env
```

#### 5. Suba os containers com o docker-compose

```
sudo docker-compose up
```


<br><br>

# Rotas

## GET /issues
#### Parameters
| Name | Type | Description |
|:----:|:----:|:-----------:|
| github_token | ```string```  | Token para acessar a API do Github |
| url | ```string```  | URL para o repositório que será analisado|
| must_have_labels | ```lista de string```  | Labels que indicam que determinada issue é uma issue de bug |
| must_not_have_labels | ```lista de string```  | Labels que indicam que determinada issue não deve ser considerada um bug |


#### Exemplo
```json
{
    "github_token": "<GITHUB TOKEN>",
    "url": "https://github.com/facebook/react",
    "must_have_labels": ["Type: Bug", "bug"],
    "must_not_have_labels": ["Status: Unconfirmed"]
}
```

GITHUB TOKEN: É preciso criar um token em https://github.com/settings/tokens, para aumentar o limite de requisições realizadas para a API do Github.

**DURANTE A CRIAÇÃO NÃO É PRECISO DE NENHUMA AUTORIZAÇÃO**



### Reponse
| Name | Type | Description |
|:----:|:----:|:-----------:|
| message | ```string```  | Mensagem para o status do processamento |
| link | ```string```  | Link para acompanhar o processamento da requisição |

#### Exemplo
```json
{
    "message": "The repository has been successfully added to the processing queue! Follow the link to check the processing status.",
    "link": "https://reliability-django.herokuapp.com/processing?status_token=72e662d5-fe11-482d-bae1-bcfb9ae1ea7d"
}
```



<br><br>

## GET /processing?status_token=<STATUS_TOKEN>

#### Exemplo
```
/processing?status_token=72e662d5-fe11-482d-bae1-bcfb9ae1ea7d
```

#### Reponse

Essa rota irá retornar o status do processamento, caso o processamento não tenha terminado.
Caso o processamento já tenha terminado, será retornado o link para a image gerada.


#### Exemplo processamento em andamento
```json
{
    "message": "This repository is still being processed. ",
    "status": {
        "ERRORS_MSG": [],
        "ERRORS": false,
        "total_of_issues": 377,
        "progress": "2.12%",
        "issues_processed": 8
    }
}
```

#### Exemplo processamento finalizado
```json
{
    "message": "The repository has been successfully added to the processing queue! Follow the link to check the processing status.",
    "link": "https://reliability-images.s3-sa-east-1.amazonaws.com/4BPIXN5UAZ.png"
}
```
