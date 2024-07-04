import psycopg2

# Configurações de conexão com o PostgreSQL
dbname = 'communityevents'
user = 'community_admin'
password = 'password'
host = 'localhost'
port = '5432'

try:
    # Conecta ao PostgreSQL
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Cria um cursor para executar operações SQL
    cur = conn.cursor()

    # Executa uma consulta SQL
    cur.execute('SELECT version()')

    # Recupera o resultado da consulta
    db_version = cur.fetchone()
    print(f'Versão do PostgreSQL: {db_version}')

    # Fecha o cursor e a conexão
    cur.close()
    conn.close()

except psycopg2.Error as e:
    print(f'Erro ao conectar ao PostgreSQL: {e}')
