# sitedelivros/models.py
from flask import current_app
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados MySQL"""
    config = current_app.config['DB_CONFIG'] # Acessa a configuração do DB a partir da app
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        return connection
    except Error as e:
        current_app.logger.error(f"Erro ao conectar ao MySQL: {e}")
        raise Exception(f"Erro ao conectar ao MySQL: {e}") # Propaga o erro

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Executa uma query no banco de dados"""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params or ()) # Usa () para params se for None

        if fetch_one:
            result = cursor.fetchone()
            return result
        elif fetch_all:
            result = cursor.fetchall()
            return result
        else:
            # Para queries DML (INSERT, UPDATE, DELETE) ou DDL
            connection.commit()
            return cursor.rowcount

    except Error as e:
        if connection:
            connection.rollback()
        current_app.logger.error(f"Erro ao executar query: {e} - Query: {query} - Params: {params}")
        raise Exception(f"Erro ao executar query: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Modifique a classe User para herdar de UserMixin
class User(UserMixin):
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    # get_id() é um método obrigatório para Flask-Login
    def get_id(self):
        return str(self.id)

    @staticmethod
    def get_by_email(email):
        query = "SELECT id, email, password_hash FROM users WHERE email = %s"
        user_data = execute_query(query, (email,), fetch_one=True)
        if user_data:
            return User(user_data['id'], user_data['email'], user_data['password_hash'])
        return None

    @staticmethod
    def get_by_id(user_id):
        query = "SELECT id, email, password_hash FROM users WHERE id = %s"
        user_data = execute_query(query, (user_id,), fetch_one=True)
        if user_data:
            return User(user_data['id'], user_data['email'], user_data['password_hash'])
        return None

    @staticmethod
    def create(email, password):
        password_hash = generate_password_hash(password)
        query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
        execute_query(query, (email, password_hash))
        # Retorna o objeto User recém-criado, buscando pelo email
        return User.get_by_email(email)


class Book:
    @staticmethod
    def get_all_by_user(user_id):
        """Retorna todos os livros de um usuário específico"""
        query = "SELECT id, title, author, year, cover_url, description FROM books WHERE user_id = %s ORDER BY title"
        return execute_query(query, (user_id,), fetch_all=True)

    @staticmethod
    def get_by_id_and_user(book_id, user_id):
        """Busca um livro pelo ID que pertence a um usuário específico"""
        query = "SELECT id, title, author, year, cover_url, description FROM books WHERE id = %s AND user_id = %s"
        return execute_query(query, (book_id, user_id), fetch_one=True)

    @staticmethod
    def create(title, author, user_id, year=None, cover_url=None, description=None):
        """Cria um novo livro para um usuário específico"""
        query = """
            INSERT INTO books (title, author, user_id, year, cover_url, description)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return execute_query(query, (title, author, user_id, year, cover_url, description))

    @staticmethod
    def update(book_id, title, author, user_id, year=None, cover_url=None, description=None):
        """Atualiza um livro existente de um usuário específico"""
        query = """
            UPDATE books
            SET title = %s, author = %s, year = %s, cover_url = %s, description = %s
            WHERE id = %s AND user_id = %s
        """
        return execute_query(query, (title, author, year, cover_url, description, book_id, user_id))

    @staticmethod
    def delete(book_id, user_id):
        """Deleta um livro de um usuário específico"""
        query = "DELETE FROM books WHERE id = %s AND user_id = %s"
        return execute_query(query, (book_id, user_id))

    # Métodos antigos mantidos para compatibilidade (podem ser removidos se não usados)
    @staticmethod
    def get_all():
        """Retorna todos os livros (método depreciado)"""
        query = "SELECT id, title, author, year, cover_url, description FROM books ORDER BY title"
        return execute_query(query, fetch_all=True)

    @staticmethod
    def get_by_id(book_id):
        """Busca um livro pelo ID (método depreciado)"""
        query = "SELECT id, title, author, year, cover_url, description FROM books WHERE id = %s"
        return execute_query(query, (book_id,), fetch_one=True)