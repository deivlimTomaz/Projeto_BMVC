# Bmvc

## Rodando projeto com o BMVC no BASH:

1. Executar o arquivo 'route.py', na raiz do projeto.

## Rodando com o BMVC no DOCKER:

1. $ docker build -t bmvci .
1. $ docker run -d -p 8080:8080 -v $(pwd):/app bmvci

Atenção: pode ser /bmeta em vez de /app
