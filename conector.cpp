#include <iostream>
#include <pqxx/pqxx>

using namespace std;
using namespace pqxx;

int main() {
    try {
        // Conectar ao banco de dados PostgreSQL
        connection C("dbname=communityevents user=seu_usuario password=sua_senha host=seu_host port=sua_porta");

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
