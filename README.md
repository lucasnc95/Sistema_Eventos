# Sistema de Eventos

Este é um projeto de sistema de eventos desenvolvido com Flask e PostgreSQL.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- [Python 3](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Pip](https://pip.pypa.io/en/stable/)

## Passo a Passo para Compilar e Executar o Programa

1. **Acesse o PostgreSQL**: Abra o terminal e execute: `sudo -i -u postgres`

2. **Acesse o console do PostgreSQL**: Digite o comando: `psql`

3. **Crie o banco de dados**: No console do PostgreSQL, execute: `CREATE DATABASE sistema_eventos;`

4. **Crie um usuário**: Crie um usuário com a senha desejada: `CREATE USER myuser WITH PASSWORD 'mypassword';`

5. **Conceda privilégios ao usuário**: Dê todas as permissões ao novo usuário no banco de dados: `GRANT ALL PRIVILEGES ON DATABASE sistema_eventos TO myuser;`

6. **Saia do console do PostgreSQL**: Digite: `\q` e depois: `exit`

7. **Crie um ambiente virtual**: No terminal, no diretório do seu projeto, execute: `python3 -m venv venv`

8. **Ative o ambiente virtual**: Ative o ambiente virtual com o seguinte comando: `source venv/bin/activate`

9. **Instale as dependências do projeto**: Instale os pacotes necessários: `pip install flask flask-sqlalchemy psycopg2-binary flask-bcrypt flask-login`

10. **Execute o aplicativo**: Finalmente, execute o aplicativo Flask: `python app.py`



