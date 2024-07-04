## Plataforma de Gerenciamento de Eventos Comunitários com Integração de Banco de Dados

### Visão Geral

Esta documentação descreve como configurar, testar e executar uma plataforma de gerenciamento de eventos comunitários que utiliza um banco de dados PostgreSQL para armazenar informações sobre eventos e mensagens entre os usuários.

### Pré-requisitos

- PostgreSQL instalado e configurado.
- Python 3.10 e ambiente virtual (`venv`) configurado.
- Bibliotecas necessárias instaladas:
  - Flask
  - Flask-SQLAlchemy
  - Psycopg2
- Biblioteca `libpqxx` para C++.

## Passo a Passo

#### 1. Configuração do Banco de Dados PostgreSQL

##### Estrutura das Tabelas

1. **Tabela `Event`**:
    - `id`: Identificador único do evento (inteiro, chave primária)
    - `name`: Nome do evento (string, não nulo)
    - `description`: Descrição do evento (texto, não nulo)
    - `date`: Data do evento (data, não nulo)

2. **Tabela `Message`**:
    - `id`: Identificador único da mensagem (inteiro, chave primária)
    - `sender`: Remetente da mensagem (string, não nulo)
    - `receiver`: Destinatário da mensagem (string, não nulo)
    - `content`: Conteúdo da mensagem (texto, não nulo)
    - `timestamp`: Carimbo de data/hora da mensagem (data e hora, padrão para a hora atual, não nulo)

##### Comandos SQL para Configuração do Banco de Dados

Execute os seguintes comandos SQL para criar o banco de dados e as tabelas:

```sql
CREATE DATABASE communityevents;
CREATE USER community_admin WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE communityevents TO community_admin;

\c communityevents

CREATE TABLE Event (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL
);

CREATE TABLE Message (
    id SERIAL PRIMARY KEY,
    sender VARCHAR(100) NOT NULL,
    receiver VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
```

#### 2. Configuração do Ambiente Python

##### Criação do Ambiente Virtual e Instalação das Dependências

No diretório do seu projeto, execute os seguintes comandos:

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install Flask Flask-SQLAlchemy psycopg2
```

> **Nota:** O diretório `myenv` será criado automaticamente após a execução do comando acima.

#### 3. Arquivo `app.py`

Crie e configure o arquivo `app.py` para a aplicação Flask:

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://community_admin:sua_senha@localhost:5432/communityevents'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    new_event = Event(name=data['name'], description=data['description'], date=data['date'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'}), 201

@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([{'id': e.id, 'name': e.name, 'description': e.description, 'date': e.date} for e in events]), 200

@app.route('/messages', methods=['POST'])
def send_message():
    data = request.get_json()
    new_message = Message(sender=data['sender'], receiver=data['receiver'], content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'}), 201

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{'id': m.id, 'sender': m.sender, 'receiver': m.receiver, 'content': m.content, 'timestamp': m.timestamp} for m in messages]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

#### 4. Testando a Conexão ao Banco de Dados com C++

Crie um arquivo `conector.cpp` com o seguinte conteúdo:

```cpp
#include <iostream>
#include <pqxx/pqxx>

using namespace std;
using namespace pqxx;

int main() {
    try {
        // Conectar ao banco de dados PostgreSQL
        connection C("dbname=communityevents user=community_admin password=sua_senha host=localhost port=5432");

        if (C.is_open()) {
            cout << "Conexão bem-sucedida com o banco de dados PostgreSQL." << endl;

            // Executar uma consulta para recuperar mensagens
            nontransaction N(C);
            result R(N.exec("SELECT id, sender, receiver, content, timestamp FROM messages"));

            // Iterar sobre o resultado da consulta
            for (result::const_iterator it = R.begin(); it != R.end(); ++it) {
                cout << "ID: " << it[0].as<int>() << endl;
                cout << "Sender: " << it[1].as<string>() << endl;
                cout << "Receiver: " << it[2].as<string>() << endl;
                cout << "Content: " << it[3].as<string>() << endl;
                cout << "Timestamp: " << it[4].as<string>() << endl << endl;
            }

            cout << "Consulta executada com sucesso." << endl;
        } else {
            cout << "Falha ao conectar ao banco de dados PostgreSQL." << endl;
            return 1;
        }

        C.disconnect();
    } catch (const std::exception &e) {
        cerr << e.what() << endl;
        return 1;
    }

    return 0;
}
```

Compile e execute o programa C++:

```bash
g++ -o conector conector.cpp -lpqxx -lpq
./conector
```

#### 5. Executando a Aplicação Flask

Para iniciar a aplicação Flask, execute o seguinte comando:

```bash
python app.py
```

#### 6. Notas Finais

- **Portas do Banco de Dados**: Certifique-se de que a porta 5432 (ou outra porta configurada) esteja aberta e acessível.
- **Arquivo `myenv`**: Este diretório será criado automaticamente ao configurar o ambiente virtual e instalar as dependências necessárias.
