# MaxApi - TCC
Este repositório visa desenvolver a API de uma solução tecnológica para a elicitação do conhecimento, que será composto por um sistema web, que integrará essa API em Python e um chatbot que também está presente neste repositório. A solução é voltada para o armazenamento dos dados em mapas conceituais estendidos (MCE), uma abordagem que permite organizar e recuperar as informações de maneira eficiente.<br>
A elicitação do conhecimento ocorre de forma automatizada por meio de perguntas estruturadas conduzidas pelo chatbot. Este processo permite que o chatbot guie o usuário através de uma série de perguntas, coletando informações relevantes para o sistema de maneira organizada. <br>
O chatbot foi denominado de `MAX` - `Management and Acquisition eXpert` e foi desenvolvido para o Trabalho de Conclusão de Curso (TCC).

<br>
<br>

## Sumário

- [Descrição](#descrição)
- [Pré-requisitos](#pré-requisitos)
- [Instalação do PostgreSQL](#instalação-do-postgresql)
  - [Windows](#windows)
  - [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
  - [macOS](#macos)
- [Configuração e Execução da API](#configuração-e-execução-da-api)
  - [Passo 1: Clonar o Repositório](#passo-1-clonar-o-repositório)
  - [Passo 2: Criar e Ativar o Ambiente Virtual](#passo-2-criar-e-ativar-o-ambiente-virtual)
  - [Passo 3: Instalar Dependências](#passo-3-instalar-dependências)
  - [Passo 4: Configuração do Banco de Dados](#passo-4-configuração-do-banco-de-dados)
  - [Passo 5: Executar a API](#passo-5-executar-a-api)
- [Configuração do Ambiente](#configuração-do-ambiente)

---

<br>
<br>

## Descrição
Esta API é a base do sistema do projeto MAX TCC. Ela contém os endpoints necessários para o sistema web e toda a lógica do chatbot. 

Os endpoints presentes nessa API são:

- GET_ALL_FOCAL_QUESTIONS
- GET_FOCAL_QUESTION
- SIGN_IN
- USER_INPUT
- CREATE_CHAT
- GET_ALL_CHAT_HISTORY

Sendo que para realizar o processo de conversa com o chatbot, será através do endpoint USER_INPUT.

Para realizar testes apenas da api, sem estar integrando com o sistema WEB, está disponível uma collection do Postman no repositório, nomeada `MAX - Chatbot - TCC.postman_collection.json`.

Para utilizar, também é necessário um banco de dados PostgreSQL configurado com o nome `max_chatbot`.

## Pré-requisitos
- Python 3.9 ou superior
- PostgreSQL
- Acesso ao terminal (ou linha de comando no Windows)

<br>
<br>

## Instalação do PostgreSQL

### Windows
1. **Baixe o instalador**: Acesse o [site oficial do PostgreSQL](https://www.postgresql.org/download/windows/) e baixe a versão mais recente.
2. **Instale o PostgreSQL**:
   - Durante a instalação, anote o usuário, a senha e a porta (geralmente `5432`) configurados, pois serão necessários para configurar o banco de dados da API.
   - Inclua o **pgAdmin** (interface gráfica para gerenciar o banco de dados), se preferir.
3. **Configuração**:
   - Abra o `pgAdmin` ou instale uma ferramenta de banco de dados (Como o `dBeaver`) e crie um banco de dados chamado `max_chatbot`.

### Linux (Ubuntu/Debian)
1. **Instale o PostgreSQL**:
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```
2. **Inicie o serviço do PostgreSQL**:
   ```bash
   sudo systemctl start postgresql
   ```
3. **Configure o usuário e o banco de dados**:
   - Entre no PostgreSQL como o usuário `postgres`:
     ```bash
     sudo -u postgres psql
     ```
   - No prompt do PostgreSQL, crie um usuário com senha:
     ```sql
     CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
     ```
   - Crie o banco de dados `max_chatbot` e dê permissões ao usuário criado.
     - Aqui, se preferir, instale uma ferramenta de banco de dados, como o `dBeaver` e faça isso por lá
     ```sql
     CREATE DATABASE max_chatbot;
     GRANT ALL PRIVILEGES ON DATABASE max_chatbot TO seu_usuario;
     ```
   - Saia do prompt do PostgreSQL:
     ```sql
     \q
     ```

### macOS
1. **Instale o PostgreSQL** usando o [Homebrew](https://brew.sh/):
   ```bash
   brew update
   brew install postgresql
   ```
2. **Inicie o PostgreSQL**:
   ```bash
   brew services start postgresql
   ```
3. **Configure o banco de dados**:
   - Acesse o PostgreSQL:
     ```bash
     psql postgres
     ```
   - Crie o usuário e o banco de dados:
     ```sql
     CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
     CREATE DATABASE max_chatbot;
     GRANT ALL PRIVILEGES ON DATABASE max_chatbot TO seu_usuario;
     ```
   - Saia do prompt do PostgreSQL:
     ```sql
     \q
     ```

<br>
<br>

## Configuração e Execução da API

### Passo 1: Clonar o Repositório
Clone este repositório para o seu ambiente local:

HTTP:
```bash
git clone https://github.com/iarav/MaxApi-TCC.git
cd MaxApi-TCC
```
OU SSH:

```bash
git clone git@github.com:iarav/MaxApi-TCC.git
cd MaxApi-TCC
```

### Passo 2: Criar e Ativar o Ambiente Virtual
1. Crie o ambiente virtual:
   ```bash
   python -m venv venv
   ```

2. Ative o ambiente virtual:
   - **No Windows**:
     ```cmd
     venv\Scripts\activate
     ```
   - **No Unix/macOS**:
     ```bash
     source venv/bin/activate
     ```

### Passo 3: Instalar Dependências
Instale as dependências do projeto usando o arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

#### Dependências Alternativas
Se ocorrerem problemas com o `requirements.txt`, instale manualmente:
```bash
pip install python-dotenv uvicorn fastapi sqlalchemy psycopg2 spacy
python -m spacy download pt_core_news_sm
```

### Passo 4: Configuração do Banco de Dados
1. **Rode o script de criação de tabelas**: Execute o script SQL localizado em `api/db/db_script` para criar as tabelas necessárias.
2. **Configure o arquivo `.env`**: Crie um arquivo `.env` na raiz do projeto e configure a variável `DATABASE_URL` no seguinte formato:
   ```
   DATABASE_URL=postgresql://USUARIO:SENHA@localhost:PORTA/max_chatbot
   ```
   - Substitua `USUARIO`, `SENHA`, `PORTA`, e `max_chatbot` conforme sua configuração do PostgreSQL.

### Passo 5: Executar a API
Para iniciar a API, execute o seguinte comando:
```bash
uvicorn api.main:app --reload
```

## Configuração do Ambiente
Este projeto foi desenvolvido e testado usando:
- **Python**: 3.11.4
- **PostgreSQL**