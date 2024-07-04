# Documentação: Configuração e Execução da Plataforma de Gerenciamento de Eventos Comunitários

## Passo a Passo Detalhado

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu_usuario/CommunityEvents.git
cd CommunityEvents
```

### 2. Criar o Ambiente Virtual

```bash
python3 -m venv myenv
```

### 3. Ativar o Ambiente Virtual

- No Linux/MacOS:
  ```bash
  source myenv/bin/activate
  ```
- No Windows:
  ```bash
  myenv\Scripts\activate
  ```

### 4. Instalar as Dependências

Crie um arquivo `requirements.txt` com o seguinte conteúdo:

```txt
Flask==2.0.2
Flask-SQLAlchemy==2.5.1
psycopg2-binary==2.9.3
```

E execute:

```bash
pip install -r requirements.txt
```

### 5. Configurar o Banco de Dados PostgreSQL

Certifique-se de que o PostgreSQL está rodando e configure um banco de dados chamado `communityevents`:

```sql
CREATE DATABASE communityevents;
CREATE USER community_admin WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE communityevents TO community_admin;
```

### 6. Configurar a Aplicação Flask

Atualize as configurações de conexão com o banco de dados no arquivo `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://community_admin:sua_senha@localhost:5432/communityevents'
```

### 7. Criar as Tabelas do Banco de Dados

```bash
python app.py
```

### 8. Compilar o Conector C++

```bash
g++ -o conector conector.cpp -lpqxx -lpq
```

### 9. Testar o Conector C++

```bash
./conector
```

### 10. Iniciar a Aplicação

```bash
python app.py
```

### 11. Acessar a Aplicação

Abra um navegador e acesse:

```
http://localhost:5000
```

## Observação sobre a Porta

Para alterar a porta padrão, modifique o arquivo `app.py`:

```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3000)  # Altere para a porta desejada
```

## Observação sobre o Diretório `myenv`

O diretório `myenv` será criado automaticamente durante o processo de configuração do ambiente virtual. Não é necessário criá-lo manualmente.

## Conclusão

Seguindo esses passos, você terá configurado e iniciado a plataforma de gerenciamento de eventos comunitários. Se houver problemas, verifique os logs de erro e certifique-se de que todas as dependências e configurações estão corretas.
