import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection(config):
    """Cria e retorna uma conexão com o banco de dados MySQL"""
    print("DEBUG: get_db_connection: Tentando conectar ao MySQL.") # Nova linha de depuração
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        print("DEBUG: get_db_connection: Conexão MySQL bem-sucedida.") # Nova linha de depuração
        return connection
    except Error as e:
        print(f"DEBUG: get_db_connection: Erro ao conectar ao MySQL: {e}") # Mais explícito
        raise # **Mantenha este raise** para garantir que o erro se propague

def execute_query(config, query, params=None, fetch_one=False, fetch_all=False):
    """Executa uma query no banco de dados"""
    # Adicionei este print para ver se a query está sendo chamada
    print(f"DEBUG: execute_query: Executando query: {query[:50]}...") # Nova linha de depuração (limitado para não poluir)
    connection = None
    cursor = None
    try:
        connection = get_db_connection(config) # Esta chamada já tem seu próprio DEBUG
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params or ())

        if fetch_one:
            result = cursor.fetchone()
            return result
        elif fetch_all:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.rowcount

    except Error as e:
        if connection:
            connection.rollback()
        print(f"DEBUG: execute_query: Erro ao executar query: {e} - Query: {query[:50]}...") # Mais explícito
        raise # **Mantenha este raise**
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def create_tables(config):
    """Cria as tabelas necessárias no banco de dados e o usuário admin padrão para NEOLIBRES"""
    print("DEBUG: create_tables: Iniciando criação de tabelas.") # Nova linha de depuração

    # Criar tabela users
    users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """
    print("DEBUG: create_tables: Executando query para users_table.") # Nova linha de depuração
    execute_query(config, users_table)

    # Criar tabela books
    books_table = """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,  # CORRIGIDO AQUI! Era NOTFENAL
            author VARCHAR(255) NOT NULL,
            year INT,
            cover_url VARCHAR(500),
            description TEXT
        )
    """
    print("DEBUG: create_tables: Executando query para books_table.") # Nova linha de depuração
    execute_query(config, books_table)

    # ... (o resto do código create_tables permanece o mesmo) ...
    admin_user = execute_query(
        config,
        "SELECT id, email, password_hash FROM users WHERE email = %s",
        ('admin@neolibres.com',),
        fetch_one=True
    )

    if not admin_user:
        admin_password_hash = generate_password_hash('admin123')
        execute_query(
            config,
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
            ('admin@neolibres.com', admin_password_hash)
        )
        print("Usuário administrador padrão 'admin@neolibres.com' criado com sucesso.")
    else:
        print("Usuário administrador 'admin@neolibres.com' já existe.")
    print("DEBUG: create_tables: Finalizado.") # Nova linha de depuração