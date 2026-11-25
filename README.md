# BMVC | Sistema de Gerenciamento de Produtos

Aplicação web desenvolvida em Python utilizando o framework Bottle e uma arquitetura organizada em modelos, controladores e visualizações.

O projeto consiste em um site de produtos de beleza que oferece um catálogo público, cadastro e autenticação de usuários e gerenciamento de produtos com controle de acesso.

O desenvolvimento foi realizado em três níveis, com a implementação progressiva das funcionalidades.

## 1. Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Backend e regras de negócio |
| Bottle | Framework web e gerenciamento de rotas |
| HTML/TPL | Estrutura das páginas e templates |
| CSS | Estilização e responsividade |
| JavaScript | Interações e pesquisa dinâmica |
| JSON | Persistência de produtos e usuários |
| Docker | Execução em ambiente containerizado |
| Git e GitHub | Versionamento do projeto |

## 2. Funcionalidades

### Gerenciamento de produtos

O sistema implementa as quatro operações do CRUD:

- **Create:** cadastro de produtos.
- **Read:** listagem e consulta de produtos.
- **Update:** atualização de informações.
- **Delete:** exclusão de produtos.

Cada produto possui os seguintes atributos:

| Atributo | Descrição |
|---|---|
| ID | Identificador único |
| Nome | Nome do produto |
| Categoria | Categoria do produto |
| Preço | Valor do produto |
| Estoque | Quantidade disponível |

Os registros são armazenados em JSON e permanecem disponíveis após a reinicialização da aplicação, desde que os arquivos de dados sejam preservados.

### Autenticação de usuários

O sistema permite:

- Cadastro de clientes.
- Login com e-mail e senha.
- Validação de credenciais.
- Gerenciamento de sessões.
- Logout.
- Consulta às informações da conta.
- Controle de acesso baseado no perfil do usuário.

As senhas são armazenadas utilizando PBKDF2-HMAC-SHA256 com salt aleatório.

### Controle de acesso

Existem dois perfis de usuários autenticados: `cliente` e `gerente`.

Além deles, visitantes não autenticados podem consultar o catálogo.

| Funcionalidade | Visitante | Cliente | Gerente |
|---|---|---|---|
| Visualizar página inicial | Sim | Sim | Sim |
| Consultar catálogo | Sim | Sim | Sim |
| Pesquisar produtos | Sim | Sim | Sim |
| Criar conta | Sim | Não | Não |
| Acessar Minha Conta | Não | Sim | Sim |
| Acessar gerenciamento | Não | Não | Sim |
| Cadastrar produtos | Não | Não | Sim |
| Editar produtos | Não | Não | Sim |
| Excluir produtos | Não | Não | Sim |

As permissões administrativas são verificadas no backend.

Um cliente não consegue acessar as operações de gerenciamento apenas digitando diretamente o endereço de uma rota administrativa.

## 3. Estrutura do projeto

```text
Projeto_BMVC/
│
├── README.md
├── .gitignore
│
└── site_vendas/
    │
    ├── route.py
    ├── criar_gerente.py
    ├── Dockerfile
    │
    ├── app/
    │   │
    │   ├── models/
    │   │   ├── produtos.py
    │   │   └── usuario.py
    │   │
    │   ├── controllers/
    │   │   ├── application.py
    │   │   ├── datarecord.py
    │   │   ├── auth.py
    │   │   │
    │   │   └── db/
    │   │       ├── produtos.json
    │   │       └── usuarios.json
    │   │
    │   ├── views/
    │   │   └── html/
    │   │       ├── inicio.tpl
    │   │       ├── catalogo.tpl
    │   │       ├── produtos.tpl
    │   │       ├── cadastro.tpl
    │   │       ├── login.tpl
    │   │       └── conta.tpl
    │   │
    │   └── static/
    │       ├── css/
    │       │   └── estilos_site.css
    │       │
    │       ├── js/
    │       │   ├── catalogo.js
    │       │   └── produtos.js
    │       │
    │       └── img/
    │
    └── tests/
        └── test_nivel3.py
```

A estrutura apresenta os principais arquivos utilizados no Nível 3. O projeto também pode conter arquivos auxiliares, estilos e testes de níveis anteriores.

## 4. Arquitetura BMVC

A aplicação distribui suas responsabilidades entre diferentes componentes.

### Models

Contém as classes responsáveis pela representação dos dados.

**`produtos.py`**

Define a classe `Produto`, seus atributos e validações.

**`usuario.py`**

Define a classe `Usuario`, incluindo suas informações de identificação e perfil de acesso.

### Controllers

Contém os componentes responsáveis pelo processamento das operações.

**`application.py`**

Faz a integração entre os dados dos produtos e os templates HTML.

**`datarecord.py`**

Implementa o CRUD de produtos e a persistência em JSON.

**`auth.py`**

Implementa o gerenciamento de usuários, a autenticação, a verificação de senhas e as sessões.

### Views

Os arquivos `.tpl` representam as páginas do sistema.

O Bottle utiliza esses templates para gerar HTML com informações fornecidas pelo backend.

### Rotas

O arquivo `route.py` recebe as requisições HTTP, verifica permissões e encaminha as operações para os componentes responsáveis.

## 5. Instalação no Linux

### Pré-requisitos

- Python 3.12 ou versão compatível.
- pip.
- Suporte a ambientes virtuais Python.
- Git.

### Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd Projeto_BMVC/site_vendas
```

Substitua `URL_DO_REPOSITORIO` pelo endereço do projeto no GitHub.

### Criar ambiente virtual

```bash
python3 -m venv .venv
```

Ativar o ambiente:

```bash
source .venv/bin/activate
```

### Instalar o Bottle

```bash
python -m pip install bottle
```

### Executar a aplicação

```bash
python route.py
```

Acesse:

```text
http://localhost:8080/inicio
```

A porta utilizada pela aplicação é `8080`.

Para encerrar o servidor, pressione `Ctrl + C` no terminal.

## 6. Execução com Docker

O projeto também possui um Dockerfile para execução containerizada.

Na pasta `site_vendas`, execute:

```bash
docker build -t bmvc-site .
```

Depois, inicie o contêiner:

```bash
docker run --rm \
  --name bmvc-site \
  -p 8080:8080 \
  -v "$(pwd):/bmeta" \
  bmvc-site
```

O volume monta a pasta da aplicação no diretório `/bmeta` do contêiner.

**Importante:** para permitir conexões pela porta publicada, o Bottle precisa escutar em `0.0.0.0` dentro do contêiner.

O projeto também precisa ter permissões adequadas para gravar nos arquivos JSON.

Se estiver utilizando Docker Compose, utilize a configuração correspondente ao seu ambiente.

## 7. Cadastro de usuários

### Criar uma conta de cliente

Acesse:

```text
http://localhost:8080/cadastro
```

Preencha o formulário com:

- Nome.
- E-mail.
- Senha.
- Confirmação de senha.

Após o cadastro, a conta recebe automaticamente o perfil `cliente`.

O usuário poderá realizar login e acessar a página Minha Conta.

### Criar uma conta de gerente

O cadastro de gerentes não está disponível pela interface pública.

Para criar uma conta administrativa, execute na pasta `site_vendas`:

```bash
python criar_gerente.py
```

O programa solicitará:

```text
Nome:
E-mail:
Senha:
Confirme a senha:
```

A senha deve conter pelo menos 10 caracteres.

A conta criada receberá o perfil `gerente`.

Se a aplicação estiver utilizando Docker, o comando deve acessar o mesmo armazenamento utilizado pelo servidor.

### Realizar login

Acesse:

```text
http://localhost:8080/login
```

Informe o e-mail e a senha cadastrados.

Após a autenticação:

- Clientes acessam a página Minha Conta.
- Gerentes recebem acesso à área de gerenciamento.

## 8. Principais rotas

| Método | Rota | Funcionalidade |
|---|---|---|
| GET | `/inicio` | Página inicial |
| GET | `/catalogo` | Catálogo público |
| GET | `/cadastro` | Formulário de cadastro |
| POST | `/cadastro` | Criar conta de cliente |
| GET | `/login` | Formulário de login |
| POST | `/login` | Autenticar usuário |
| GET | `/conta` | Informações da conta |
| POST | `/logout` | Encerrar sessão |
| GET | `/produtos` | Gerenciamento administrativo |
| POST | `/produtos/adicionar` | Cadastrar produto |
| POST | `/produtos/editar/<id>` | Atualizar produto |
| POST | `/produtos/excluir/<id>` | Excluir produto |

As operações administrativas exigem autenticação com perfil `gerente`.

Os formulários que modificam dados também utilizam proteção CSRF.

## 9. Persistência dos dados

O projeto utiliza arquivos JSON para armazenar produtos e usuários.

### Produtos

Arquivo:

```text
app/controllers/db/produtos.json
```

Exemplo:

```json
[
    {
        "id": 1,
        "nome": "Sabonete Líquido",
        "categoria": "Cuidados da pele",
        "preco": 5.0,
        "estoque": 10
    }
]
```

A classe `DataRecord` realiza a leitura e a gravação dos registros.

### Usuários

Arquivo:

```text
app/controllers/db/usuarios.json
```

O repositório de usuários gerencia o cadastro, a consulta e a autenticação das contas.

Esse arquivo contém informações das contas cadastradas e não deve ser enviado ao GitHub.

### Sessões

As sessões são mantidas na memória do servidor.

Por isso, reiniciar o processo Python encerra as sessões existentes, mas não remove as contas persistidas no JSON.

## 10. Segurança

A aplicação implementa mecanismos básicos de proteção:

- Hash de senhas com PBKDF2-HMAC-SHA256.
- Salt aleatório para as senhas.
- Verificação das credenciais no backend.
- Controle de acesso baseado em perfis.
- Proteção CSRF nos formulários.
- Cookies de sessão com atributo `HttpOnly`.
- Criação administrativa de gerentes pelo terminal.
- Validação de dados recebidos pelos formulários.

**Limitações:** o projeto foi desenvolvido para fins acadêmicos e demonstração local.

Para disponibilização pública, seriam necessárias medidas adicionais, incluindo HTTPS, limitação de tentativas de login, expiração de sessões, revisão de segurança e armazenamento adequado para acessos concorrentes.

## 11. Testes

O projeto possui testes automatizados para funcionalidades do backend.

Na pasta `site_vendas`, execute:

```bash
python -m tests.test_nivel3
```

### Testes manuais

Verifique os seguintes comportamentos:

1. Um visitante consegue consultar o catálogo.
2. Um cliente consegue criar uma conta e fazer login.
3. Um cliente consegue acessar Minha Conta.
4. Um cliente não consegue acessar o gerenciamento.
5. Um gerente consegue cadastrar produtos.
6. Um gerente consegue editar produtos.
7. Um gerente consegue excluir produtos.
8. A pesquisa dinâmica funciona.
9. O logout encerra a sessão.
10. Os dados persistem após reiniciar a aplicação.

## 12. Evolução do projeto

### Nível 1

Estrutura inicial do site utilizando o código BMVC.

Implementação das primeiras páginas e organização dos arquivos do projeto.

### Nível 2

Implementação do modelo `Produto` e das operações CRUD.

Integração entre Python, Bottle e templates HTML/TPL.

Adição de persistência JSON, estilos CSS e funcionalidades JavaScript.

### Nível 3

Implementação do modelo `Usuario`.

Adição de cadastro, login, sessões, logout e controle de acesso.

Separação entre catálogo público e gerenciamento administrativo.

Criação de contas de gerente por comando no terminal.

## 13. Limitações atuais

O projeto ainda não implementa:

- Carrinho de compras.
- Processamento de pagamentos.
- Gerenciamento de pedidos.
- Recuperação de senha por e-mail.
- Controle de estoque vinculado a vendas.

O objetivo atual é demonstrar a integração entre os componentes BMVC, a manipulação de objetos Python, o CRUD e o controle de acesso de usuários.

## 14. Finalidade

Projeto acadêmico desenvolvido para demonstrar conhecimentos em programação orientada a objetos, desenvolvimento web com Python, persistência de dados, autenticação de usuários e integração entre backend e frontend.
